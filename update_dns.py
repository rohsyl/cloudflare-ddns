import requests
import os
import ast
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

CLOUDFLARE_EMAIL = os.getenv('CLOUDFLARE_EMAIL')
CLOUDFLARE_API_KEY = os.getenv('CLOUDFLARE_API_KEY')
ZONE_IDS = ast.literal_eval(os.getenv('ZONE_ID'))  # List of zone IDs


def get_public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    response.raise_for_status()
    ip = response.json()['ip']
    return ip


def get_dns_record(zone_id, record_id):
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}'
    api_key_type = identify_cloudflare_key(CLOUDFLARE_API_KEY)
    headers = get_headers(api_key_type)
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def update_dns_record(zone_id, record_id, record_name, ip):
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}'
    api_key_type = identify_cloudflare_key(CLOUDFLARE_API_KEY)
    headers = get_headers(api_key_type)
    data = {
        'type': 'A',
        'name': record_name,
        'content': ip,
        'ttl': 1,
        'proxied': True,
    }
    response = requests.put(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def get_headers(api_key_type):
    if api_key_type == 'Global API Key':
        return {
            'X-Auth-Email': CLOUDFLARE_EMAIL,
            'X-Auth-Key': CLOUDFLARE_API_KEY,
            'Content-Type': 'application/json',
        }
    elif api_key_type == 'API Token':
        return {
            'Authorization': f'Bearer {CLOUDFLARE_API_KEY}',
            'Content-Type': 'application/json',
        }
    else:
        raise ValueError('Unknown API key type')


def identify_cloudflare_key(api_key):
    """
    Identifies whether a given Cloudflare key is a Global API Key or an API Token.

    Args:
        api_key (str): The Cloudflare key to be identified.

    Returns:
        str: 'Global API Key' if the key matches the pattern for a Global API Key,
             'API Token' if the key matches the pattern for an API Token,
             'Unknown' if it does not match any known patterns.
    """
    # Check length and format for Global API Key
    if len(api_key) == 37 and all(c in 'abcdef0123456789' for c in api_key):
        return 'Global API Key'

    # Check format for API Token
    if len(api_key) == 40 and all(c.isalnum() or c in '-_' for c in api_key[4:]):
        return 'API Token'

    return 'Unknown'


def main():
    try:
        current_ip = get_public_ip()
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        for zone_id in ZONE_IDS:
            # Extract DNS records for the current zone ID from environment variables
            dns_records_var_name = f'DNS_RECORDS_{zone_id[-6:]}'  # Last 6 characters of the zone ID
            dns_records = ast.literal_eval(os.getenv(dns_records_var_name))

            for record_id, record_name in dns_records:
                dns_record = get_dns_record(zone_id, record_id)
                dns_ip = dns_record['result']['content']

                if current_ip != dns_ip:
                    print(f"[{current_date}] IP for {record_name} has changed from {dns_ip} to {current_ip}, updating DNS record.")
                    update_response = update_dns_record(zone_id, record_id, record_name, current_ip)
                    if update_response['success']:
                        print(f"[{current_date}] DNS record for {record_name} updated successfully.")
                    else:
                        print(f"[{current_date}] Failed to update DNS record for {record_name}: {update_response}")
                else:
                    print(f"[{current_date}] IP address for {record_name} has not changed.")
    except Exception as e:
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{current_date}] An error occurred: {e}")


if __name__ == '__main__':
    main()
