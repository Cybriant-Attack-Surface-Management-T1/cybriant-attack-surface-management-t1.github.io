""" Imports """
import socket  # base
import ssl  # base
import sys  # base
import dns.resolver  # dnspython

def get_server_certificates(domain: str) -> str:
    """
    This function takes in a domain as a parameter and creates a socket that connects to the domain.
    Once the socket has been formed, the domains certificates are then queried.

    :param domain: the domain to be queried
    :type domain: str
    :return: The certs belonging to the domain
    :rtype: [str]
    """

    print(f'Searching for certificates for {domain}')
    certificates = []
    default_context = ssl.create_default_context()

    # Socket creation
    with socket.create_connection((domain, 443)) as sock:

        # Binding the socket to the domain
        with default_context.wrap_socket(sock, server_hostname=domain) as ssock:
            # Grabbing the certificates
            certificate = ssock.getpeercert()

            '''
            These two will grab the binary form of the certificate. This is useful if the actual certificate is needed
            
            full_certificate = ssock.getpeercert(binary_form=True)
            pem_certificate = ssl.DER_cert_to_PEM_cert(full_certificate)
            '''
            print(f'Cipher: {ssock.cipher()}')
            print(f'Version: {ssock.version()}')
            print(f'Certificate found: {certificate}')
            certificates.append(certificate)
    return certificate


def check_NSEC(records: [str]) -> str:
    nsec_records = None
    if records is not None:
        for record in records:
            nsec_records = record.to_text()
    return nsec_records


def check_DMARC(records: [str]) -> str:
    dmarc_record = None
    if records is not None:
        for record in records:
            dmarc_record = record.strings
            dmarc_record = dmarc_record[0].decode('utf-8')
    return dmarc_record


def check_DKIM(records: [str]) -> str:
    dkim_record = None
    if records is not None:
        for record in records:
            dkim_record = record.strings
            dkim_record = dkim_record[0].decode('utf-8')
    return dkim_record


def check_SPF(records: [str]) -> str:
    spf_record = None
    if records is not None:
        for record in records:
            if record.strings[0].startswith(b'v=spf1'):
                spf_record = record.strings[0]
    return spf_record


def get_record(domain: str, types: str) -> [str]:
    # special_types = ['SPF', 'DMARC', 'DKIM']
    # regular_types = ['A', 'AAAA', 'TXT', 'MX', 'CNAME']

    # Checking for NSEC records
    if types == 'NSEC':
        print('Checking domain for NSEC records...')
        try:
            records = dns.resolver.resolve(domain, 'NSEC')
        except Exception as e:
            print(f'No NSEC records found due to {e}.')
            return None
        print('...Done.')
        return records

    # Checking for SPF records
    elif types == 'SPF':
        print('Checking domain for SPF records...')
        try:
            records = dns.resolver.resolve(domain, 'TXT')
        except Exception as e:
            print(f'No SPF records found due to {e}.')
            return None
        print('...Done')
        return records

    # Checking for DMARC records
    elif types == 'DMARC':
        print('Checking domain for DMARC records...')
        dmarc_record = f'_dmarc.{domain}'
        try:
            records = dns.resolver.resolve(dmarc_record, 'TXT')
        except Exception as e:
            print(f'No DMARC records found due to {e}.')
            return None
        print("...Done")
        return records

    # Checking for DKIM records
    elif types == 'DKIM':
        print('Checking domain for DKIM records...')
        selector = 'default'
        dkim_record = f'{selector}._domainkey.{domain}'
        try:
            records = dns.resolver.resolve(dkim_record, 'TXT')
            print("...Done")
            return records
        except Exception as e:
            print(f'No DKIM records found due to {e}.')
            return None
    else:
        print('Invalid file type')
        return None


def main(domain: str):
    # Fetching the records for the domain
    spf_records = get_record(domain, 'SPF')
    dmarc_records = get_record(domain, 'DMARC')
    dkim_records = get_record(domain, 'DKIM')

    # Checking the records for SPF capabilities
    spf_record = check_SPF(spf_records)
    print(f'SPF record for {domain} : {spf_record}')

    # Checking the records for DMARC capabilities
    dmarc_record = check_DMARC(dmarc_records)
    print(f'DMARC record for {domain} : {dmarc_record}')

    # Checking the records for DKIM capabilities
    dkim_record = check_DKIM(dkim_records)
    print(f'DKIM record for {domain} : {dkim_record}')

    # after enumeration of the a / aaaa records for the ports, if https server found check TLS/SSL certifications and
    # implementations -> bool (True/False), *IF TRUE* (str (common name), str (expiration date))
    certificates = get_server_certificates(domain)
    if len(certificates) > 0:
        print(f'Certificate found for {domain}')
        for header in certificates:
            print(f'{header}: {certificates[header]}')


if __name__ == '__main__':
    domain = sys.argv[1]
    main(domain)
