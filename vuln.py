import nmap
import subprocess
from tqdm import tqdm

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

if __name__ == "__main__":
    while True:
        print("\nMenu:")
        print("1. Port Scan with Version Detection (-sV)")
        print("2. Stealth Scan (-sS)")
        print("0. Exit")

        choice = input("Enter your choice (0-2): ")

        if choice == '0':
            break
        elif choice == '1':
            target_ip = input("Enter the target IP address: ")
            vulnerabilities_found = port_scan(target_ip, '-p 1-65535 -sV')

            if vulnerabilities_found:
                print("\nThe server is vulnerable.")
        elif choice == '2':
            target_ip = input("Enter the target IP address: ")
            vulnerabilities_found = port_scan(target_ip, '-sS')

            if vulnerabilities_found:
                print("\nThe server is vulnerable.")
        else:
            print("Invalid choice. Please enter a valid option.")

