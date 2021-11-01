#!/user/bin/python3

import os
import sys
import json
import requests
import subprocess
import urllib3


if not len(sys.argv[1:]):
    print("[!] Usage: ./header_enum.py [target domain]")
    sys.exit(1)

target = sys.argv[1]
kill = "[!] CTRL+c received, exiting."

try:
    amass = subprocess.check_output(["which", "amass"]).rstrip()
    amass = str(amass, 'utf-8')
except:
    print("""
    [!] You need to install amass. If it is already installed,
        then you need to add it to your $PATH variable.
    """)
    sys.exit(1)


def amass_enum():
    global kill
    print("""
    [*] Gathering subdomains, this may take a while.. Press CTRL+c to quit..
    """)
    try:
        os.system(f'{amass} enum -d {target} -silent -noalts -o {target}.targets')
    except KeyboardInterrupt:
        print(kill)
        sys.exit(0)
    except Exception as e:
        print(f"[!] Error received: {e}")
        sys.exit(0)


def enum_headers():
    global kill
    global target
    try:
        targets = str(f"{target}.targets")
        with open(targets) as target_list:
            for t in target_list:
                try:
                    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                    t = t.rstrip()
                    r=requests.get(f"http://{t}", verify=False, timeout=5)
                    print(f"\nHTTP - {t}:")
                    print(json.dumps(dict(r.headers)))
                    rs=requests.get(f"https://{t}", verify=False, timeout=5)
                    print(f"\nHTTPS - {t}:")
                    print(json.dumps(dict(rs.headers)))
                except Exception as e:
                    #print(f"[!] Error received: {e}")
                    continue
                except KeyboardInterrupt:
                    print(kill)
                    sys.exit(0)
    except KeyboardInterrupt:
        print(kill)
    except Exception as e:
        print(f"[!] Error received: {e}")


def main():
    try:
        amass_enum()
        enum_headers()
    except Exception as e:
        print(f"[!] Error received: {e}")

main()
