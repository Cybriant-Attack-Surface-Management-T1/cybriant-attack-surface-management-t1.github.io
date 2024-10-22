import nmap # base
import csv # base
from datetime import datetime

"""
    -This function will take input from a text file
        file.txt: contains list of domains and subdomains
    -The script will be connected to our google cloud
    
    -Each port listed on the txt file will be scanned with ports 1-12,000

    -Aggregate this data and place it in a formatted csv file
        The format: 
        
    -This function will output the information into a new csv file
        ports.csv: containes list of domains and open ports
    
"""

def scan_ports(domain):
    # Create a PortScanner instance
    nm = nmap.PortScanner()

    try:
        # Scan the target for open ports
        print(f"Scanning {domain}...")
        nm.scan(domain, arguments='-p-')  # Scan ports 1 to 1024

        # Check if the scan was successful
        if nm.all_hosts():
            for host in nm.all_hosts():
                print(f'\nHost: {host} ({nm[host].hostname()})')
                print(f'State: {nm[host].state()}')

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
        else:
            print(f"No hosts found for {domain}.")
    except Exception as e:
        print(f"Error scanning {domain}: {str(e)}")

    return open_ports


def main():

    domains = []
    # Read the domains from a file
    with open('sample_domains.txt', 'r') as f:
        domains = [line.strip() for line in f.readlines()]

    results = []

    for domain in domains:
        open_ports = scan_ports(domain)
        results.append((domain, open_ports))

    # Create CSV filename with today's date
    date_str = datetime.now().strftime("%m_%d_%Y")
    csv_filename = f'port_scan_{date_str}.csv'

    # Write results to CSV
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Domain', 'Open Ports'])
        for domain, ports in results:
            writer.writerow([domain, ', '.join(map(str, ports))])

    print(f"Scanning complete. Results saved to {csv_filename}.")

if __name__ == "__main__":
    main()