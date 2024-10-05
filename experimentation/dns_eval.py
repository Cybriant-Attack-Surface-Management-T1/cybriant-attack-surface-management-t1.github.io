""" Imports """
import whois  # python-whois
import sys  # base


def get_domain_info(domain: str) -> {str}:
    """
    This function finds information about the domain using the whois tool and stores it in a list
    :param domain: The domain to query
    :type domain: str
    :return: Information about the domain
    :rtype: dict
    """
    domain_info = {}

    # try-except statement to look for domain information
    try:
        domain_i = whois.whois(domain)
        domain_info['Domain'] = domain_i.domain  # redundant domain name return
        domain_info['Registrar'] = domain_i.registrar  # domains registrar
        domain_info['Creation date'] = domain_i.creation_date  # domains creation date
        domain_info['Expiration date'] = domain_i.expiration_date  # domains expiration date
        domain_info['Emails'] = domain_i.emails  # emails attached to domain

    # Bare exception catch
    except Exception as e:
        print(f'Error: {e}')
        return None
    return domain_info


def main(domain: str):
    """
    Main function that calls the domain information function
    :param domain: The domain to query
    :type domain: str
    """
    domain_info = get_domain_info(domain)
    if domain_info:
        print(domain_info)


if __name__ == '__main__':
    domain = sys.argv[1]
    main(domain)
