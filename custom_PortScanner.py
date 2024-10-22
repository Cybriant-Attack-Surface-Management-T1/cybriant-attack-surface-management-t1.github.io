import sys # base
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
    nm = nmap.PortScanner()
    
    try:
        print(f"Scanning {domain}...")
        nm.scan(domain, arguments='-p 1-1024')  # Scan ports 1 to 1024

        # Check if the scan was successful
        if nm.all_hosts():
            open_ports = []
            for proto in nm[domain].all_protocols():
                lport = nm[domain][proto].keys()
                for port in sorted(lport):
                    if nm[domain][proto][port]['state'] == 'open':
                        open_ports.append(port)
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