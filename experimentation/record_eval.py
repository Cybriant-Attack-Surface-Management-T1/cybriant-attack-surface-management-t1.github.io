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
    :return: Certificates belonging to the domain
    :rtype: list of str
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
            print('Certificate found')
            print(f'Cipher: {ssock.cipher()}')
            print(f'Version: {ssock.version()}')

            certificates.append(certificate)
    return certificate


def check_NSEC(records: [str]) -> str:
    """
    This function parses the NSEC records if found and turns them into a text format
    :param records: The records to be checked
    :type records: list of str
    :return: NSEC records in text format
    :rtype: str
    """
    print("Parsing NSEC records")
    nsec_records = None
    if records:
        nsec_records = records.to_text()
    return nsec_records


def check_DMARC(records: [str]) -> str:
    """
    This function parses the DMARC records if found decodes them into a text format
    :param records: The records to be checked
    :type records: list of str
    :return: DMARC records in text format
    :rtype: str
    """
    print("Parsing DMARC records")

    dmarc_record = None
    if records:
        dmarc_record = records.strings
        dmarc_record = dmarc_record[0].decode('utf-8')
    return dmarc_record


def check_DKIM(records: [str]) -> str:
    """
    This function parses the DKIM records if found decodes them into a text format
    :param records: The records to be checked
    :type records: list of str
    :return: DKIM records in text format
    :rtype: str
    """
    print("Parsing DKIM records")
    dkim_record = None
    if records:
        dkim_record = records.strings
        dkim_record = dkim_record[0].decode('utf-8')
    return dkim_record


def check_SPF(records: [str]) -> str:
    """
    This function filters the records for the SPF containing line.
    :param records: The records to be checked
    :type records: list of str
    :return: SPF records in text format
    :rtype: str
    """
    print("Parsing records for SPF")
    spf_record = None
    if records:
        if records.strings[0].startswith(b'v=spf1'):
            spf_record = records.strings[0]
    return spf_record


def get_record(domain: str, types: str) -> [str] or None:
    """
    This function takes a domain and the type of record to look for as parameters. Those are then used to run the
    corresponding path and look through the records for the type that matches the passed in 'types' parameter.
    :param domain: The domain to be queried
    :type domain: str
    :param types: The type of record to look for
    :type types: str
    :return: The records corresponding to the types parameter
    :rtype: list of str
    :return: None placeholder if no records are found for the type
    :rtype: None
    """
    # special_types = ['SPF', 'DMARC', 'DKIM']
    # regular_types = ['A', 'AAAA', 'TXT', 'MX', 'CNAME']

    # Checking for NSEC records
    if types == 'NSEC':
        print('Checking domain for NSEC records.')
        try:
            records = dns.resolver.resolve(domain, 'NSEC')

        # Bare exception catch
        except Exception as e:
            print(f'No NSEC records found due to {e}.')
            return None
        return records

    # Checking for SPF records
    elif types == 'SPF':
        print('Checking domain for SPF records.')
        try:
            records = dns.resolver.resolve(domain, 'TXT')

        # Bare exception catch
        except Exception as e:
            print(f'No SPF records found due to {e}.')
            return None
        return records

    # Checking for DMARC records
    elif types == 'DMARC':
        print('Checking domain for DMARC records...')
        dmarc_record = f'_dmarc.{domain}'  # common format dmarc records
        try:
            records = dns.resolver.resolve(dmarc_record, 'TXT')

        # Bare exception catch
        except Exception as e:
            print(f'No DMARC records found due to {e}.')
            return None
        return records

    # Checking for DKIM records
    elif types == 'DKIM':
        print('Checking domain for DKIM records.')
        selector = 'default'  # base selector to query for
        dkim_record = f'{selector}._domainkey.{domain}'  # common format for dkim records
        try:
            records = dns.resolver.resolve(dkim_record, 'TXT')
            print("...Done")
            return records

        # Bare exception catch
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
    if spf_record:
        print(f'SPF record for {domain} : {spf_record}')

    # Checking the records for DMARC capabilities
    dmarc_record = check_DMARC(dmarc_records)
    if dmarc_record:
        print(f'DMARC record for {domain} : {dmarc_record}')

    # Checking the records for DKIM capabilities
    dkim_record = check_DKIM(dkim_records)
    if dkim_record:
        print(f'DKIM record for {domain} : {dkim_record}')

    # after enumeration of the a / aaaa records for the ports, if https server found check TLS/SSL certifications and
    # implementations -> bool (True/False), *IF TRUE* (str (common name), str (expiration date))

    certificates = get_server_certificates(domain)  # this will work if the domain is attached to a https connecting
    # site

    if len(certificates) > 0:
        print(f'Certificate found for {domain}')
        for header in certificates:
            print(f'{header}: {certificates[header]}')


if __name__ == '__main__':
    domain = sys.argv[1]
    main(domain)
