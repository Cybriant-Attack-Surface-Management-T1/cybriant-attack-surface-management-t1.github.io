import ssl
import socket
import subprocess
import csv
import dns.resolver
import re
import idna


# Function to find SPF records
def get_spf_record(domain):
    try:
        dns_txt = dns.resolver.resolve(domain, 'TXT')
        for txt in dns_txt:
            records = txt.to_text()
            if "v=spf1" in records:
                return records
        return "No SPF record"
    except(dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.DNSException):
        return "No SPF record"

# Function to find DKIM records
def get_dkim_record(domain):
    try:
        dkim_name = f'default._domainkey.{domain}'
        dkim_txt = dns.resolver.resolve(dkim_name, 'TXT')
        for txt in dkim_txt:
            dkim = txt.to_text()
            return dkim
    except(dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.DNSException):
        return "No DKIM record"

# Function to find DMARC record
def get_dmarc_record(domain):
    try:
        dmarc_name = f'_dmarc.{domain}'
        dmarc_txt = dns.resolver.resolve(dmarc_name, 'TXT')
        for txt in dmarc_txt:
            return txt
    except(dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.DNSException):
        return "No DMARC record"

# Function to find TLS/SSL certificate details
def get_tls_details(domain):
    try:
        context = ssl.create_default_context()

        with socket.create_connection((domain, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=domain) as ssock:

                cert = ssock.getpeercert()
                return ssock.version(), cert
    except (UnicodeError, socket.gaierror):
        return "No TLS/SSL details"

# Function to check for DNSSEC
def get_dnssec_status(domain):
    try:
        # Checks to see if DNSKEY exists which indicates DNSSEC is enabled.
        dnssec = dns.resolver.resolve(domain, dns.rdatatype.DNSKEY)
        if dnssec.rrset:
            return "DNSSEC is enabled"

    except(dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.exception.DNSException):
        return "DNSSEC is not enabled"

# Function to check for domain squatting
def check_domain_squatting(domain):
    try:
        #Generates a couple of hundred or thousand permutations of domain names and singles out the registered ones.
        result = subprocess.run(['dnstwist', '-r', domain], capture_output=True, text=True, encoding='utf-8')
        #This finds the domains in the output.
        squat = re.findall(r'(?<=\s)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?=\s)', result.stdout)
        if squat:
            #This removes the first entry in the list because it is the original domain.
            squat.pop(0)

        # Returns the list of domain squatting threats.
        return squat
    except subprocess.SubprocessError:
        return "No threats exist"

# Function to convert domain to Punycode
def convert_to_punycode(domain):
    try:
        return idna.encode(domain).decode('ascii')
    except UnicodeError:
        return "No punycode"


# List of domains to check
domains = ["wcostream.tv", "google.com", "amazon.com", "microsoft.com", "example.com", "cloudflare.com", "yahoo.com", "gmail.com", "facebook.com", "kennesaw.edu"]

# Create CSV file and add header
with open('domain_metrics.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Domain", "SPF Record", "DKIM Record", "DMARC Record", "TLS Details", "DNSSEC Status", "Domain Squatting Threats", "Punycode"])


    # Loop through each domain and gather metrics
    for domain in domains:
        spf_record = get_spf_record(domain)
        dkim_record = get_dkim_record(domain)
        dmarc_record = get_dmarc_record(domain)
        tls_details = get_tls_details(domain)
        dnssec_status = get_dnssec_status(domain)
        domain_squatters = check_domain_squatting(domain)
        punycode = convert_to_punycode(domain)

        # Write to CSV
        writer.writerow(
            [domain, spf_record, dkim_record, dmarc_record, tls_details, dnssec_status, domain_squatters, punycode])
