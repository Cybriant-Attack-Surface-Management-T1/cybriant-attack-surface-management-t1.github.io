import nmap # base
import csv # base
from datetime import datetime
from urllib.parse import urlparse  # Import to help extract the root domain

"""
    -This function will take input from a text file
        domains.txt: contains list of domains and subdomains

    -The script will be connected to our google cloud
    
    -Each port listed on the txt file will be scanned from all ports

    -Aggregate this data and place it in a formatted csv file
        The format: domain, root domain, host ip, host state, open ports list
        
    -This function will output the information into a new csv file
        ports.csv: contains list of domains and their open ports
    
"""

def get_root_domain(domain):
    # Parse the domain and extract the root domain
    parsed_uri = urlparse(f'http://{domain}')
    return parsed_uri.netloc


def scan_ports(domain):
    # Create a PortScanner instance
    nm = nmap.PortScanner()

    try:
        # Scan the domain for open ports
        print(f"Scanning {domain}...")
        nm.scan(domain, arguments='-p-')  # Scan all ports, "-P- means all ports"


        # Check if the scan was successful
        if nm.all_hosts():
            for host in nm.all_hosts():
                host_state = nm[host].state()
                root_domain = get_root_domain(domain)
                host_ip={host}

                print(f'\nHost: {host} ({root_domain})')
                print(f'State: {host_state}')

                # Get open ports
                open_ports = []
                for proto in nm[host].all_protocols():
                    lport = nm[host][proto].keys()
                    for port in sorted(lport):
                        if nm[host][proto][port]['state'] == 'open':
                            open_ports.append(port)

                if open_ports:
                    print(f'Open ports: {open_ports}')
                else:
                    print('No open ports found.')

                # Return host info and open ports
                return host_ip, root_domain, host_state, open_ports
            
        else:
            print(f"No hosts found for {domain}.")
            return None, None, None, []
        
    except Exception as e:
        print(f"Error scanning {domain}: {str(e)}")
        return None, None, None, []

    

def main():
    # Read the domains from a file
    with open('sample_domains.txt', 'r') as f:
        domains = [line.strip() for line in f.readlines()]

    results = []

    # Scan each domain
    for domain in domains:
        root_domain, host_ip, host_state, open_ports = scan_ports(domain)
        # Only add results if a valid host was found
        if root_domain is not None:
            results.append((domain, host_ip, root_domain, host_state, open_ports))

    # Create CSV filename with today's date
    date_str = datetime.now().strftime("%m_%d_%Y")
    csv_filename = f'port_scan_{date_str}.csv'

    # Write results to CSV
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Domain','Root Domain','Host IP','State', 'Open Ports'])
        for domain, host_ip, root_domain, host_state, ports in results:
            writer.writerow([domain, host_ip, root_domain, host_state,', '.join(map(str, ports))])

    print(f"Scanning complete. Results saved to {csv_filename}.")

if __name__ == "__main__":
    main()