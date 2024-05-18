import requests
import os
import ast
from dotenv import load_dotenv

load_dotenv()

CLOUDFLARE_EMAIL = os.getenv('CLOUDFLARE_EMAIL')
CLOUDFLARE_API_KEY = os.getenv('CLOUDFLARE_API_KEY')
ZONE_ID = os.getenv('ZONE_ID')
DNS_RECORDS = ast.literal_eval(os.getenv('DNS_RECORDS'))


def get_public_ip():
    response = requests.get('https://api.ipify.org?format=json')
    response.raise_for_status()
    ip = response.json()['ip']
    return ip


def get_dns_record(record_id):
    url = f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{record_id}'
    headers = {
        'X-Auth-Email': CLOUDFLARE_EMAIL,
        'X-Auth-Key': CLOUDFLARE_API_KEY,
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def update_dns_record(record_id, record_name, ip):
    url = f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{record_id}'
    headers = {
        'X-Auth-Email': CLOUDFLARE_EMAIL,
        'X-Auth-Key': CLOUDFLARE_API_KEY,
        'Content-Type': 'application/json',
    }
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


def main():
    try:
        current_ip = get_public_ip()

        for record_id, record_name in DNS_RECORDS:
            dns_record = get_dns_record(record_id)
            dns_ip = dns_record['result']['content']

            if current_ip != dns_ip:
                print(f"IP for {record_name} has changed from {dns_ip} to {current_ip}, updating DNS record.")
                update_response = update_dns_record(record_id, record_name, current_ip)
                if update_response['success']:
                    print(f"DNS record for {record_name} updated successfully.")
                else:
                    print(f"Failed to update DNS record for {record_name}: {update_response}")
            else:
                print(f"IP address for {record_name} has not changed.")
    except Exception as e:
        print("An error occurred:", e)


if __name__ == '__main__':
    main()
