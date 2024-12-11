# Public IP Update Script for Cloudflare DNS Records

This Python script checks if your public IP address has changed and updates the corresponding A records in Cloudflare DNS if necessary.

## Purpose

The script is designed for users who manage their own hosting servers and use Cloudflare for DNS management. It ensures that the DNS records in Cloudflare are always up-to-date with the current public IP address, which is particularly useful for users without a static IP.

## Requirements

- Python 3.x
- `requests` library
- `python-dotenv` library

## Setup and Usage

### 1. Install Dependencies

First, make sure you have Python 3.x installed. Then, install the required Python libraries using pip:

```sh
pip install requests python-dotenv
```

### 2. Get your Cloudflare API Key

- Log in your Cloudflare account and go to "My Profile" -> "API Tokens"
- View your "Global API Key" and save it for later

### 3. Get zone id and records ids

Get your zones using Cloudflare API
```
curl -X GET "https://api.cloudflare.com/client/v4/zones" \
-H "Content-Type: application/json" \
-H "X-Auth-Email: <your-email-address>" \
-H "X-Auth-Key: <your-global-api-key>"
```

Get dns records of a zone using Cloudflare API
```
curl -X GET "https://api.cloudflare.com/client/v4/zones/<zone-id>/dns_records" \
-H "Content-Type: application/json" \
-H "X-Auth-Email: <your-email-address>" \
-H "X-Auth-Key: <your-global-api-key>"
```

### 4. Create a .env File
Create a .env file in the same directory as your script and add your Cloudflare API credentials and DNS records information. The .env file should look like this:

```env
CLOUDFLARE_EMAIL=your-email@example.com
CLOUDFLARE_API_KEY=your-api-key
ZONE_ID=["your-zone-id-d41f54"]
DNS_RECORDS_d41f54=[("dns-record-id-1", "example.com"), ("dns-record-id-2", "sub.example.com")]
```
> `ZOME_ID` is an array of the zones you want to work with.
>
> You need to add an entry `DNS_RECORDS_[...]` in the .env for each zone and append **the last 6 char of the zone id**.

### 5. Run the Script
Run the script using Python:

```sh
python update_dns.py
```

## Automate the Script

You can automate this script to run at regular intervals using a task scheduler like cron on Linux or Task Scheduler on Windows.

Exemple to run the script every 5 minutes using CRON :
```
*/5 * * * * /usr/bin/python3 /path/to/your/script/update_dns.py >> /path/to/your/logfile.log 2>&1
```

## License
This project is licensed under the MIT License.
