""" Imports """
import whois  # python-whois
import sys  # base


def get_domain_info(domain: str) -> [str]:
    domain_info = []
    try:
        domain_i = whois.whois(domain)
        domain_info.append(f'Domain: {domain_i.domain}')
        domain_info.append(f'Registrar: {domain_i.registrar}')
        domain_info.append(f'Creation date: {domain_i.creation_date}')
    except Exception as e:
        print(f'Error: {e}')
    return domain_info


def main(domains: str):
    domain_info = get_domain_info(domains)
    print(domain_info)


if __name__ == '__main__':
    domain = sys.argv[1]
    main(domain)
