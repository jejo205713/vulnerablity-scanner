import nmap
import subprocess
from tqdm import tqdm

# ANSI escape codes for green color
GREEN = "\033[92m"
RESET = "\033[0m"

def port_scan(target_ip, arguments):
    nm = nmap.PortScanner()
    nm.scan(hosts=target_ip, arguments=arguments)

    exploits_found = []

    for host in nm.all_hosts():
        print(f"Open ports for {host}:")
        for proto in nm[host].all_protocols():
            ports = nm[host][proto].keys()

            # Initialize tqdm progress bar
            total_ports = len(list(ports))
            progress_bar = tqdm(ports, desc="Scanning ports", unit="port", colour='green')

            for port in progress_bar:
                service = nm[host][proto][port]
                print(f"Port {port}/{proto} is open. Service: {service['name']}")

                # Check for exploits using searchsploit
                exploit_search_result = search_exploit(service['name'], service['version'])
                if exploit_search_result:
                    exploits_found.extend([(port, version) for version in exploit_search_result])

    return exploits_found

def search_exploit(service_name, service_version):
    search_command = f"searchsploit '{service_name} {service_version}'"
    
    try:
        result = subprocess.check_output(search_command, shell=True, text=True)
        exploits_found = result.strip().split('\n')
        return exploits_found
    except subprocess.CalledProcessError:
        print("Error searching for exploits.")
        return []

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
            exploits = port_scan(target_ip, '-p 1-65535 -sV')

            if exploits:
                print("\nVulnerable Versions Found:")
                for port, version in exploits:
                    print(f"Port {port} - Vulnerable Version: {version}")
        elif choice == '2':
            target_ip = input("Enter the target IP address: ")
            port_scan(target_ip, '-sS')
        else:
            print("Invalid choice. Please enter a valid option.")

