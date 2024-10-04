""" Imports """
import sys  # base
import dns.resolver  # dnspython


def check_NSEC(records: [str]) -> str:
    nsec_records = None
    if records is not None:
        for record in records:
            nsec_records = record.to_text()
    return nsec_records


def get_record(domain: str, types: str) -> [str]:
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

    # Checking for DNSSEC records
    elif types == 'DNSSEC':
        print('Checking domain for DNSSEC records...')
        dns_keys = None
        dns_ds = None
        dns_rrsig = None

        print('Checking for a DNSKEY file...')
        try:
            dnssec_records = dns.resolver.resolve(domain, 'DNSKEY')
            print('Found DNSKEY...')
            for record in dnssec_records:
                dns_keys = record
        except Exception as e:
            print(f'...No DNSKEY records found due to {e}.')

        print('Checking for DS file...')
        try:
            dnssec_records = dns.resolver.resolve(domain, 'DS')
            print('Found DS...')
            for record in dnssec_records:
                dns_ds = record
        except Exception as e:
            print(f'...No DS records found due to {e}.')

        print('Checking for RRSIG file...')
        try:
            dnssec_records = dns.resolver.resolve(domain, 'RRSIG')
            print('Found RRSIG...')
            for record in dnssec_records:
                dns_rrsig = record
        except Exception as e:
            print(f'...No RRSIG records found due to {e} error.')

        print('Finished checking for DNSSEC records.')
        return dns_keys, dns_ds, dns_rrsig
    else:
        print('Invalid file type')
        return None


def main(domain: str):
    # Fetching the records from the domain
    nsec_records = get_record(domain, 'NSEC')
    dnssec_records = get_record(domain, 'DNSSEC')

    # Checking the NSEC records for list of DNS capabilities
    nsec_records = check_NSEC(nsec_records)
    print(f'NSEC records for {domain}: {nsec_records}')

    print(f'DNSSEC records for {domain}: {dnssec_records}')


if __name__ == '__main__':
    domain = sys.argv[1]
    main(domain)
