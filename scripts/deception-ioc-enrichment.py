# Import the requests module so we can make HTTP calls to the AbuseIPDB API
# Run "pip install requests" in your terminal if you don't have it
import requests

# Import the csv module so we can read the input CSV file
# csv is part of Python's standard library - no installation needed
import csv

# Import the time module so we can pause between API calls
# time is part of Python's standard library - no installation needed
import time

import os


# ── YOUR SETTINGS ─────────────────────────────────────────────────────────────

# Your AbuseIPDB API key - regenerate this as it was exposed earlier
API_KEY = os.environ.get("AbuseIP")

# The path to your CSV file
# If it is in the same folder as this script, just put the filename
INPUT_FILE = "alerts.csv"

# The exact name of the column in your CSV that contains the IP addresses
# Must match the column header exactly including capitalisation
IP_COLUMN = "IPAddress"

# The file to write the results to
OUTPUT_FILE = "enrichment.txt"


# ── STEP 1: READ THE IP ADDRESSES FROM THE CSV ────────────────────────────────

# Open the CSV file in read mode
with open(INPUT_FILE, "r", encoding="utf-8") as infile:

    # DictReader reads each row as a dictionary where the keys are column headers
    # e.g. row["IPAddress"] gives you the IP address for that row
    reader = csv.DictReader(infile)

    # Loop through every row and pull out the IP address column
    # This builds a list of every IP in the file
    # .strip() removes any accidental spaces around the value
    ip_list = [row[IP_COLUMN].strip() for row in reader]

# Remove any duplicate IPs so we don't call the API more than once per IP
# set() removes duplicates, list() converts it back to a list
ip_list = list(set(ip_list))

print(f"Found {len(ip_list)} unique IP addresses to look up")

# ── STEP 2: LOOK UP EACH IP AND STORE THE RESULTS ────────────────────────────

results = []

for ip in ip_list:

    print(f"Looking up {ip}...")

    url = "https://api.abuseipdb.com/api/v2/check"
    headers = {"Key": API_KEY, "Accept": "application/json"}
    params = {"ipAddress": ip, "maxAgeInDays": 90}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()["data"]

    results.append(data)

    time.sleep(1.5)

# ── STEP 3: SORT BY CONFIDENCE SCORE - HIGHEST FIRST ─────────────────────────

results = sorted(results, key=lambda r: r.get("abuseConfidenceScore", 0), reverse=True)

# ── STEP 4: WRITE SORTED RESULTS TO FILE ─────────────────────────────────────

with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:

    for data in results:

        score = data.get("abuseConfidenceScore", 0)

        outfile.write(f"─────────────────────────────────\n")
        outfile.write(f"IP Address:        {data.get('ipAddress')}\n")
        outfile.write(f"Confidence Score:  {score} / 100\n")
        outfile.write(f"Total Reports:     {data.get('totalReports')}\n")
        outfile.write(f"Country:           {data.get('countryCode')}\n")
        outfile.write(f"Usage Type:        {data.get('usageType')}\n")
        outfile.write(f"ISP:               {data.get('isp')}\n")
        outfile.write(f"Is Whitelisted:    {data.get('isWhitelisted')}\n")
        outfile.write(f"Last Reported:     {data.get('lastReportedAt')}\n")
        outfile.write(f"\n")

        if score > 20:
            outfile.write(f"⚠ FLAGGED - SCORE ABOVE 20\n")

print(f"\nDone. Results saved to {OUTPUT_FILE}")
