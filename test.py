import nmap

def scan_ports(target):
    # Create a PortScanner instance
    nm = nmap.PortScanner()

    try:
        # Scan the target for open ports
        print(f"Scanning {target}...")
        nm.scan(target, arguments='-p 1-1024')  # Scan ports from 1 to 1024

        # Check if the host is up
        if nm.all_hosts():
            for host in nm.all_hosts():
                print(f'\nHost: {host} ({nm[host].hostname()})')
                print(f'State: {nm[host].state()}')

                # Get open ports
                open_ports = []
                for proto in nm[host].all_protocols():
                    lport = nm[host][proto].keys()
                    for port in lport:
                        if nm[host][proto][port]['state'] == 'open':
                            open_ports.append(port)

                if open_ports:
                    print(f'Open ports: {open_ports}')
                else:
                    print('No open ports found.')

        else:
            print(f"{target} is not reachable.")

    except Exception as e:
        print(f"Error scanning {target}: {e}")

if __name__ == "__main__":
    # Change 'example.com' to the target you want to scan
    target = 'example.com'
    scan_ports(target)
