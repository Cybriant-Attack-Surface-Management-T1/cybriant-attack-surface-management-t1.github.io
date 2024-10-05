""" Imports """
import socket  # base
import ssl  # base
import sys  # base
import csv  # base
import dns.resolver  # dnspython

def get_items(records: dns.resolver.Answer) -> dict:
    """
    This function iterates through the record's answer to get the items attribute.

    :param records: Records to iterate through
    :type records: dns.resolver.Answer

    :return: Dictionary containing the filter answer
    :rtype: dict
    """
    answer = None
    items = None

    if records:
        chaining_result = getattr(records, 'chaining_result', None)
        if chaining_result:
            answer = getattr(chaining_result, 'answer', None)
        if answer:
            items = getattr(answer, 'items', None)
    return items

def store_data(record: dict or None, record_type: str, data_list: list):
    """
    This function stores data in a dict format to the passed in list.
    If no data is found in the record, a value of 'None' is assigned to that type.

    :param record: The record to be used  as the value.
    :type record: list or None

    :param record_type: The type of record to be used as the key.
    :type record_type: str

    :param data_list: The list containing the data to be stored.
    :type data_list: list
    """

    if record:
        data_list.append({record_type: record.strings[0]})
    else:
        data_list.append({record_type: 'None'})


def create_csv(DOMAIN: str, data: list):
    """
    This function aggregates the dictionary data before creating a csv file out of the data.

    :param DOMAIN: Domain name to be used in the creation of the file
    :type DOMAIN: str

    :param data: Dictionary containing the data to be used
    :type data: list
    """
    unique_keys = set()

    # loop to create a set of the dict keys
    for item in data:
        unique_keys.update(item.keys())

    consolidated_data = {}

    # nested loop to iterate through the data and consolidate it
    for key in unique_keys:
        for item in list(data):
            if key in item:
                if key in consolidated_data:

                    # appends results to key if key already exists in consolidated data
                    if isinstance(consolidated_data[key], list):
                        consolidated_data[key].append(item[key])
                    else:
                        consolidated_data[key] = [consolidated_data[key], item[key]]
                else:
                    consolidated_data[key] = item[key]
                data.remove(item)  # removes data from original list to shorten sequential search iterations

    # Crating the csv file
    csv_file = f"{DOMAIN}-record-eval.csv"
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=unique_keys)
        writer.writeheader()
        writer.writerow(consolidated_data)


def get_server_certificates(DOMAIN: str) -> dict:
    """
    This function takes in a domain as a parameter and creates a socket that connects to the domain.
    Once the socket has been formed, the domains certificates are then queried.

    :param DOMAIN: the domain to be queried
    :type DOMAIN: str

    :return: Certificates belonging to the domain
    :rtype: list of str
    """
    print(f'Searching for certificates for {DOMAIN}')

    certificates = {}
    default_context = ssl.create_default_context()

    # Socket creation
    with socket.create_connection((DOMAIN, 443)) as sock:
        # Binding the socket to the domain
        with default_context.wrap_socket(sock, server_hostname=DOMAIN) as ssock:

            # Grabbing the certificates
            certificate = ssock.getpeercert()

            '''
            These two will grab the binary form of the certificate. This is useful if the actual certificate is needed
            
            full_certificate = ssock.getpeercert(binary_form=True)
            pem_certificate = ssl.DER_cert_to_PEM_cert(full_certificate)
            '''

            if certificate:
                print('Certificate found')

                # print(f'Cipher: {ssock.cipher()}')
                certificates['Cipher'] = ssock.cipher()
                certificates['Cipher'] = certificates['Cipher'][0]  # Quick override to only store the cipher

                # print(f'Version: {ssock.version()}')
                certificates['Version'] = ssock.version()

                for header in certificate:
                    certificates[header] = certificate[header]
    return certificates


def check_DMARC(records: list) -> str:
    """
    This function parses the DMARC records if found decodes them into a text format.

    :param records: The records to be checked
    :type records: list of str

    :return: DMARC records in text format
    :rtype: str
    """
    print("Parsing DMARC records")

    dmarc_record = None

    items = get_items(records)
    if items:
        for item in items:
            if item.strings[0].startswith(b'v=DMARC'):
                dmarc_record = item
                break
    return dmarc_record


def check_DKIM(records: list) -> str:
    """
    This function parses the DKIM records if found decodes them into a text format.

    :param records: The records to be checked
    :type records: list of str

    :return: DKIM records in text format
    :rtype: str
    """
    print("Parsing DKIM records")

    dkim_record = None

    items = get_items(records)
    if items:
        for item in items:
            if item.strings[0].startswith(b'v=DKIM'):
                dkim_record = item
                break
    return dkim_record


def check_SPF(records: list) -> str:
    """
    This function filters the records for the line containing the SPF.

    :param records: The records to be checked
    :type records: list of str

    :return: SPF records in text format
    :rtype: str
    """
    print("Parsing records for SPF")

    spf_record = None

    items = get_items(records)
    if items:
        for item in items:
            if item.strings[0].startswith(b'v=spf1'):
                spf_record = item
                break
    return spf_record


def get_record(DOMAIN: str, record_type: str) -> list or None:
    """
    This function takes a domain and the type of record to look for as parameters. Those are then used to run the
    corresponding path and look through the records for the type that matches the passed in 'types' parameter.

    :param DOMAIN: The domain to be queried
    :type DOMAIN: str

    :param record_type: The type of record to look for
    :type record_type: str

    :return: The records corresponding to the types parameter
    :rtype: list of str

    :return: None placeholder if no records are found for the type
    :rtype: None
    """

    # Checking for SPF records
    if record_type == 'SPF':
        print('Checking domain for SPF records.')
        try:
            records = dns.resolver.resolve(DOMAIN, 'TXT')

        # Bare exception catch
        except Exception as e:
            print(f'No SPF records found due to {e}.')
            return None
        return records

    # Checking for DMARC records
    elif record_type == 'DMARC':
        print('Checking domain for DMARC records...')
        dmarc_record = f'_dmarc.{DOMAIN}'  # common format for dmarc records
        try:
            records = dns.resolver.resolve(dmarc_record, 'TXT')

        # Bare exception catch
        except Exception as e:
            print(f'No DMARC records found due to {e}.')
            return None
        return records

    # Checking for DKIM records
    elif record_type == 'DKIM':
        print('Checking domain for DKIM records.')
        selector = 'default'  # base selector to query for
        dkim_record = f'{selector}._domainkey.{DOMAIN}'  # common format for dkim records
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


def main(DOMAIN: str):
    csv_data = []

    # Fetching the records for the domain
    spf_records = get_record(DOMAIN, 'SPF')
    dmarc_records = get_record(DOMAIN, 'DMARC')
    dkim_records = get_record(DOMAIN, 'DKIM')

    # Checking the records for SPF capabilities
    spf_record = check_SPF(spf_records)
    store_data(spf_record, 'SPF', csv_data)

    # Checking the records for DMARC capabilities
    dmarc_record = check_DMARC(dmarc_records)
    store_data(dmarc_record, 'DMARC', csv_data)

    # Checking the records for DKIM capabilities
    dkim_record = check_DKIM(dkim_records)
    store_data(dkim_record, 'DKIM', csv_data)

    # Checking the domain for certificates
    certificates = get_server_certificates(DOMAIN)  # this will work if the domain is attached to a https connecting
    # site

    # for loop that iterates through rows that have multiple data points.
    if certificates:
        for key, value in certificates.items():
            if isinstance(value, tuple) or isinstance(value, list) or isinstance(value, dict):
                if len(value) > 1:
                    for item in value:
                        csv_data.append({key: item})
                else:
                    csv_data.append({key: value})
            else:
                csv_data.append({key: value})

    # calling the csv file creation function
    create_csv(DOMAIN, csv_data)


if __name__ == '__main__':
    DOMAIN = sys.argv[1]
    main(DOMAIN)
