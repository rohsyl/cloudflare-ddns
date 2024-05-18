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

### 2. Create a .env File
Create a .env file in the same directory as your script and add your Cloudflare API credentials and DNS records information. The .env file should look like this:

```env
CLOUDFLARE_EMAIL=your-email@example.com
CLOUDFLARE_API_KEY=your-api-key
ZONE_ID=your-zone-id
DNS_RECORDS=[("dns-record-id-1", "example.com"), ("dns-record-id-2", "sub.example.com")]
```

### 4. Run the Script
Run the script using Python:

```sh
python update_dns.py
```

## Automate the Script

You can automate this script to run at regular intervals using a task scheduler like cron on Linux or Task Scheduler on Windows.

## License
This project is licensed under the MIT License.