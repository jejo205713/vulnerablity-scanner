import nmap
import os
import subprocess
from tqdm import tqdm
from datetime import datetime
import cowsay
from alive_progress import alive_bar

# INTRO - ASCII Art
def print_ascii_art():
    os.system("figlet 'WEB-PROWLER'")
    print("####################################################################################################################")
    print("#  The script scans the target IP and checks whether it has any open ports and whether it could be exploited...🚀  #")
    print("####################################################################################################################")
    print("⚠ CAUTION: It is only for educational purposes, not to be used unethically...!")
    print("CREDITS:\n 🚀 JEJO_J \n 🚀 PADMESH_PS \n 🚀 PRIYADHARSHAN_V")

# Risk level calculation based on service names and ports
def calculate_risk(service_name, port):
    high_risk_services = ['ftp', 'telnet', 'http', 'smb', 'rdp']
    medium_risk_services = ['ssh', 'https', 'pop3']
    if port in [21, 23, 80, 3389]:  # Example of high-risk ports
        return 'Critical'
    if service_name in high_risk_services:
        return 'High'
    elif service_name in medium_risk_services:
        return 'Medium'
    else:
        return 'Low'

# Check Exploit Database for vulnerabilities
def check_exploits(service):
    product = service.get('product')
    version = service.get('version')
    if not product or not version:
        print("Product or version information not available for exploitation check.")
        return False

    if subprocess.call("which searchsploit", shell=True) != 0:
        print("Error: searchsploit is not installed.")
        return False

    print(f"Checking Exploit Database for {product} {version}...")
    search_result = subprocess.run(['searchsploit', f'{product} {version}'], stdout=subprocess.PIPE, text=True)

    if search_result.returncode == 0:
        exploits = search_result.stdout.strip().split('\n')
        if exploits:
            print("Possible exploits found:")
            for exploit in exploits[:10]:  # Limit to top 10 results
                print(exploit)
            return True  # Vulnerability found
        else:
            print("No exploits found.")
    else:
        print("Error occurred while searching Exploit Database.")

    return False  # No vulnerability found

# Scan function with final report
def port_scan(target_ip, arguments, scan_type, report_filename):
    # Check if Nmap is installed
    if subprocess.call("which nmap", shell=True) != 0:
        print("Error: Nmap is not installed. Please install Nmap and try again.")
        return [], False

    nm = nmap.PortScanner()
    try:
        nm.scan(hosts=target_ip, arguments=arguments)
    except Exception as e:
        print(f"Error during scan: {str(e)}")
        return [], False

    if not nm.all_hosts():
        print("No hosts found during the scan. Please check the target IP.")
        return [], False

    scan_data = []
    vulnerabilities_found = False  # Initialize the variable here

    for host in tqdm(nm.all_hosts(), desc="Scanning hosts", unit="host", total=len(nm.all_hosts())):
        open_ports = []
        for proto in nm[host].all_protocols():
            ports = nm[host][proto].keys()
            with alive_bar(len(ports), title=f"Scanning ports for {host}", bar='blocks') as bar:
                for port in ports:
                    service = nm[host][proto][port]
                    service_name = service.get('name', 'unknown')  # Handle missing service name
                    risk_level = calculate_risk(service_name, port)
                    open_ports.append({'port': port, 'service': service_name, 'risk': risk_level, 'host': host})

                    # Check for exploits and update vulnerabilities_found
                    if check_exploits(service):
                        vulnerabilities_found = True  # Update if any exploit is found
                    bar()  # Update the progress bar

        scan_data.extend([
            {'host': host, 'port': port_info['port'], 'service': port_info['service'], 'risk': port_info['risk']}
            for port_info in open_ports
        ])

    generate_report(scan_data, report_filename)
    return scan_data, vulnerabilities_found

# Generate and save the report
def generate_report(report_data, filename):
    if not report_data:
        print("No open ports to report.")
        return

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open(filename, 'w') as report_file:
            report_file.write("FINAL REPORT\n")
            report_file.write(f"Generated on: {current_time}\n")
            report_file.write("===================================\n")
            for entry in report_data:
                report_file.write(f"Host: {entry['host']}\n")
                report_file.write(f"Port {entry['port']} - Service: {entry['service']} - Risk: {entry['risk']}\n")
                report_file.write("===================================\n")
        print(f"Report saved to {filename}")
    except IOError as e:
        print(f"Failed to save the report: {str(e)}")

# Display final report on console (with date and time)
def display_final_report(report_data):
    if not report_data:
        print("No data available for the final report.")
        return

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("\n======== FINAL REPORT ========")
    print(f"Generated on: {current_time}")
    for entry in report_data:
        print(f"\nHost: {entry['host']}")
        print(f"Port {entry['port']} - Service: {entry['service']} - Risk: {entry['risk']}")
        print("===================================")

# Check for root privileges
def check_root_permissions():
    if os.geteuid() != 0:
        print("You need to run this script with root privileges for the Stealth Scan (-sS)!")
        return False
    return True

# Show cowsay message with different animals based on the message
def show_cowsay_message(message):
    try:
        cowsay.cow(message)
    except Exception as e:
        print(f"Error displaying cowsay message: {str(e)}")

# MAIN FUNCTION
if __name__ == "__main__":
    print_ascii_art()  # Print Figlet ASCII art
    summary_report = {'Quick Scan': [], 'Full Scan': [], 'Stealth Scan': []}

    while True:
        print("\nMenu:")
        print("1. Quick Scan (Top 1000 ports)")
        print("2. Full Scan (All 6000 ports)")
        print("3. Stealth Scan (-sS)")
        print("4. nslookup")
        print("0. Exit")

        try:
            choice = int(input("Enter your choice (0-4): "))  # Validate user input
        except ValueError:
            show_cowsay_message('Invalid choice. Please enter a valid option.')
            continue

        if choice == 0:
            # Generate and display the transposed summary report
            print("\n======== FINAL SUMMARY REPORT ========")
            for scan_type, scan_data in summary_report.items():
                print(f"\n{scan_type}:")
                display_final_report(scan_data)
            break

        elif choice == 1:
            target_ip = input("Enter the target IP address: ")
            scan_data, vulnerabilities_found = port_scan(target_ip, '-p 1-1000 -sV', 'Quick Scan', 'scan_report_1000_ports.txt')
            summary_report['Quick Scan'].extend(scan_data)
            if vulnerabilities_found:
                show_cowsay_message('There are vulnerabilities in the network!')
            display_final_report(scan_data)

        elif choice == 2:
            target_ip = input("Enter the target IP address: ")
            scan_data, vulnerabilities_found = port_scan(target_ip, '-p 1-6000 -sV', 'Full Scan', 'scan_report_6000_ports.txt')
            summary_report['Full Scan'].extend(scan_data)
            if vulnerabilities_found:
                show_cowsay_message('There are vulnerabilities in the network!')
            display_final_report(scan_data)

        elif choice == 3:
            if not check_root_permissions():
                continue  # Skip this choice if root permissions aren’t available
            target_ip = input("Enter the target IP address: ")
            scan_data, vulnerabilities_found = port_scan(target_ip, '-sS', 'Stealth Scan', 'scan_report_stealth.txt')
            summary_report['Stealth Scan'].extend(scan_data)
            if vulnerabilities_found:
                show_cowsay_message('There are vulnerabilities in the network!')
            display_final_report(scan_data)

        elif choice == 4:
            domain = input("Enter the domain name: ")
            try:
                ip = subprocess.check_output(['nslookup', domain])
                print(ip.decode('utf-8'))
                show_cowsay_message(f"Domain IP found: {domain}")
            except subprocess.CalledProcessError as e:
                show_cowsay_message(f"Error finding IP for domain: {domain}")

        else:
            show_cowsay_message('Invalid choice. Please enter a valid option.')
