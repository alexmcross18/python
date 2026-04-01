import json
import os
import argparse
import requests
from azure.identity import ClientSecretCredential

# Sets up the argument parser with a description of what the script does
parser = argparse.ArgumentParser(description="Parse a custom log .txt file into JSON format and ingest into Sentinel via DCE.")
# Adds an input argument and makes it a requirement for the user to enter
parser.add_argument("--input", required=True, help="Path to the input log .txt file")
# Adds DCE arguments - all required
parser.add_argument("--dce", required=True, help="DCE endpoint URL")
parser.add_argument("--dcr", required=True, help="DCR immutable ID")
parser.add_argument("--stream", required=True, help="DCR stream name")
# Parses the command-line arguments and stores them as attributes on "args" (e.g. args.input, args.dce)
args = parser.parse_args()

# Opens the logs file in read mode and assigns the "lines" variable to read each line
with open(args.input, "r") as input_file:
    lines = input_file.readlines()

# Creates an empty list to add to later
parsed_logs = []

# Creates a for loop that removes the new line character "\n" (.strip()) from the end of each line
# Splits each line on every space (.split(" ")) a maximum of 5 times
for line in lines:
    # Silently skips blank lines
    if not line.strip():
        continue
    # Try/Except to handle error handling - skips malformed or missing lines without crashing the script
    try:
        split_logs = line.strip().split(" ", 4)
        # Creates a dictionary of key/value pairs and adds it to the parsed_logs list
        parsed_logs.append({
            "TimeGenerated": f"{split_logs[0]}T{split_logs[1]}Z",
            "log_time": split_logs[1],
            "level": split_logs[2],
            "source": split_logs[3],
            "message": split_logs[4]
        })
    except IndexError:
        # Catches lines that exist but don't have enough fields to parse
        print(f"Skipping malformed line (too few fields): {line.strip()}")
    except Exception as e:
        # Catches anything unexpected (encoding issues, memory errors, etc.) without crashing the script
        print(f"Skipping line due to unexpected error {line.strip()}")

tenant_id = os.environ.get("AZURE_TENANT_ID")
client_id = os.environ.get("AZURE_CLIENT_ID")
client_secret = os.environ.get("AZURE_CLIENT_SECRET")

print(f"Parsed {len(parsed_logs)} records from {args.input}")

# Authenticates to Azure using the service principal credentials
credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret
)

# Requests a Bearer token scoped to Azure Monitor
token = credential.get_token("https://monitor.azure.com/.default").token

# Builds the DCE ingestion URL from the provided arguments
url = f"{args.dce}/dataCollectionRules/{args.dcr}/streams/{args.stream}?api-version=2023-01-01"

# Sets the request headers with the Bearer token and content type
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Posts the parsed logs to the DCE endpoint and raises an exception if it fails
response = requests.post(url, headers=headers, json=parsed_logs)

# Checks the HTTP status code and if it is a failure raises a HTTPError
response.raise_for_status()
print(f"Successfully posted {len(parsed_logs)} records to DCE")
