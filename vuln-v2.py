import nmap
import os
import subprocess
from tqdm import tqdm

# Function to print Figlet ASCII art
def print_ascii_art():
    os.system("cowsay 'Vulnerability Scanner'")
    print("CAUTION: Re-run the script with root privilege!")
    print("The script scans the target IP range and checks whether it has any open ports and whether it could be exploited...!")
    print("CREDITS: DEDSEC-TEAM...!")

def port_scan(target_ip, arguments):
    nm = nmap.PortScanner()
    nm.scan(hosts=target_ip, arguments=arguments)

    vulnerabilities_found = False

    for host in nm.all_hosts():
        print(f"Open ports for {host}:")
        for proto in nm[host].all_protocols():
            ports = nm[host][proto].keys()

            # Initialize tqdm progress bar
            total_ports = len(list(ports))
            progress_bar = tqdm(ports, desc=f"Scanning ports for {host}", unit="port")

            for port in progress_bar:
                service = nm[host][proto][port]
                print(f"Port {port}/{proto} is open. Service: {service['name']}, Version: {service['product']} {service['version']}")
                vulnerabilities_found |= check_exploits(service)

    return vulnerabilities_found

def check_exploits(service):
    product = service['product']
    version = service['version']

    if product and version:
        print(f"Checking Exploit Database for {product} {version}...")
        search_result = subprocess.run(['searchsploit', f'{product} {version}'], stdout=subprocess.PIPE, text=True)

        if search_result.returncode == 0:
            exploits = search_result.stdout.strip().split('\n')
            if exploits:
                print("Possible exploits found:")
                for exploit in exploits:
                    print(exploit)
                return True  # Vulnerability found
            else:
                print("No exploits found.")
        else:
            print("Error occurred while searching Exploit Database.")
    else:
        print("Product or version information not available for exploitation check.")

    return False  # No vulnerability found

def vuln_scan(target_ip):
    nm = nmap.PortScanner()
    nm.scan(hosts=target_ip, arguments="--script vuln")
    print("It's a large scan and takes around 4-5 minutes...!")

    for host in nm.all_hosts():
        print(f"Vulnerability scan results for {host}:")
        for script in nm[host]['scripts']:
            print(f"Script: {script}, Output: {nm[host]['scripts'][script]}")

if __name__ == "__main__":
    print_ascii_art()  # Print Figlet ASCII art
    while True:
        print("\nMenu:")
        print("1. Port Scan with Version Detection (-sV)")
        print("2. Stealth Scan (-sS)")
        print("3. nslookup")
        print("4. Vulnerability Scan")
        print("0. Exit")

        choice = input("Enter your choice (0-4): ")

        if choice == '0':
            break
        elif choice == '1':
            target_ip = input("Enter the target IP address: ")
            vulnerabilities_found = port_scan(target_ip, '-p 1-1000 -sV')

            if vulnerabilities_found:
                os.system("cowsay 'The server is vulnerable...!'")
        elif choice == '2':
            target_ip = input("Enter the target IP address: ")
            vulnerabilities_found = port_scan(target_ip, '-sS')

            if vulnerabilities_found:
                os.system("cowsay 'The server is vulnerable...!'")
        elif choice == '3':
            target = input("Enter website name or IP: ")
            os.system(f"nslookup {target}")
        elif choice == '4':
            target_ip = input("Enter the target IP address: ")
            vuln_scan(target_ip)
        else:
            os.system("cowsay 'Invalid choice. Please enter a valid option...!'")

