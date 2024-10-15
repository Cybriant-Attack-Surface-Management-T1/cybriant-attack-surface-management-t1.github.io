import socket
from concurrent.futures import ThreadPoolExecutor

# Attempt to establish connection
def scan_port(domain, port):
    try: 
        # This is where we want to establish a socket connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result= s.connect_ex((domain, port))
            if result== 0:
                return port
    except Exception as e:
        return None
    return None


# Function to scan all ports on a single domain ports 1-49151 or 1-1024
def scan_ports(domain, port_range=(1, 1024)):
    open_ports= []
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures= [executor.submit(scan_port, domain, port) for port in range(port_range[0], port_range[1]+1)]
        for future in futures:
            port= future.result()
            if port:
                open_ports.append(port)
    return open_ports

# Check the open ports on the list of domains provided
# May want to change to pulling from txt file with domain names
if __name__=="__main__":
    domains= ["yamaha-motor.com","kennesaw.edu", "google.com"]
    for domain in domains:
        open_ports= scan_ports(domain)
        print(f"Open ports on {domain}: {open_ports}")