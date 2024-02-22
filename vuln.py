import nmap
import subprocess

def port_scan(target_ip, arguments):
    nm = nmap.PortScanner()
    nm.scan(hosts=target_ip, arguments=arguments)

    exploits_found = []

    for host in nm.all_hosts():
        print(f"Open ports for {host}:")
        for proto in nm[host].all_protocols():
            ports = nm[host][proto].keys()
            for port in ports:
                service = nm[host][proto][port]
                print(f"Port {port}/{proto} is open. Service: {service['name']}, Version: {service['product']} {service['version']}")

                # Check for exploits using searchsploit
                exploit_search_result = search_exploit(service['name'], service['version'])
                if exploit_search_result:
                    exploits_found.extend(exploit_search_result)

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
                print("\nPossible Exploits Found:")
                for exploit in exploits:
                    print(exploit)
        elif choice == '2':
            target_ip = input("Enter the target IP address: ")
            port_scan(target_ip, '-sS')
        else:
            print("Invalid choice. Please enter a valid option.")

