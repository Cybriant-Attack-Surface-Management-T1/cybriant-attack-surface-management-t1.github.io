import socket
import google.cloud.bigquery as bigquery
import os

# Combine the 2 former port scan methods
def scan_ports(domain):
    try:
        open_ports = []
        for port in range(1, 1024):  # Attempt scanning ports 1-49151 or 1-1024
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((domain, port))            # connect_ex()      vs connect()
            if result == 0:                                     # connect=flag==1   vs no connection=flag==0
                open_ports.append(port)
            sock.close()
    except Exception as e:
        return None        
    return open_ports

# Add BigQuery connection and upload
def upload_to_bigquery(domain, open_ports):
    # Enter bigQuery client details
    client = bigquery.Client()
    dataset_id = 'your_dataset_id'      
    table_id = 'your_table_id'
    table_ref = client.dataset(dataset_id).table(table_id)
    table = client.get_table(table_ref)

    rows_to_insert = [(domain, open_ports)]
    errors = client.insert_rows_json(table, [{'domain': domain, 'open_ports': open_ports}])

    if errors:
        print(f"Errors while inserting data into BigQuery: {errors}")
    else:
        print(f"Data successfully inserted into BigQuery for domain: {domain}")

if __name__ == '__main__':
    domains= ["kennesaw.edu", "google.com", "yamaha-motor.com"]
    for domain in domains:
        domain_to_scan = os.getenv('DOMAIN_TO_SCAN', domain)
        open_ports = scan_ports(domain_to_scan)
        upload_to_bigquery(domain_to_scan, open_ports)