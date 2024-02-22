import nmap
from tqdm import tqdm
import time

def perform_vuln_scan(target):
    nm = nmap.PortScanner()

    # Perform a service version detection scan
    print("Running service version detection scan...")
    with tqdm(total=100, desc="Scanning", unit="%", position=0) as pbar:
        nm.scan(target, arguments='-sV')
        pbar.update(50)  # Update progress bar halfway

    # Perform a vulnerability scan
    print("Running vulnerability scan...")
    with tqdm(total=50, desc="Scanning", unit="%", position=0) as pbar:
        nm.scan(target, arguments='--script vuln')
        pbar.update(50)  # Update progress bar to completion

    # Print scan results
    for host in nm.all_hosts():
        print(f"Host: {host}")
        print(f"State: {nm[host].state()}")
        for proto in nm[host].all_protocols():
            print(f"Protocol: {proto}")
            ports = nm[host][proto].keys()
            for port in ports:
                print(f"Port: {port}\tState: {nm[host][proto][port]['state']}\tService: {nm[host][proto][port]['name']}")
                if 'scripts' in nm[host][proto][port]:
                    scripts = nm[host][proto][port]['scripts']
                    for script_name, script_output in scripts.items():
                        print(f"  {script_name}: {script_output}")

if __name__ == "__main__":
    target_address = input("Enter the target network address (e.g., 192.168.1.1): ")
    perform_vuln_scan(target_address)

