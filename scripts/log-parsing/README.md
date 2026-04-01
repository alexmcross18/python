# .txt Log Parser — Log Analytics Workspace/Sentinel Pipeline
A Python script that parses plain text log files and ingests the structured data directly into a
Log Analytics Workspace/Sentinel table via an Azure Data Collection Endpoint (DCE).

---

## What it does
- Reads a plain text log file supplied via the `--input` argument
- Parses each line into structured fields: TimeGenerated, log_time, level, source, and message
- Handles blank lines, malformed records, and unexpected errors without crashing
- Authenticates to Azure using a service principal via environment variables — no stored credentials
- POSTs the parsed records as a JSON payload to an Azure DCE endpoint
- Data lands in a custom Log Analytics Workspace table queryable via KQL in Sentinel

---

## Files
| File                  | Description                                        |
|-----------------------|----------------------------------------------------|
| .txt-file-parsing.py  | Main parser and ingestion script                   |
| logs.txt              | Sample log file (input)                            |
| sample.json           | Sample JSON payload used when creating the DCR table |

---

## Prerequisites
- Python 3
- An Azure Log Analytics Workspace with Sentinel enabled
- A Data Collection Endpoint (DCE)
- A Data Collection Rule (DCR) linked to the DCE and a custom table (`CustomTableName`)
- A service principal with the **Monitoring Metrics Publisher** role assigned on the DCR

---

## Setup

### 1. Install dependencies
```
pip install azure-identity requests
```

### 2. Create a service principal
1. Go to Entra ID - App Registrations
2. Click on "New Registration"
3. Enter a name and click "Register"
4. Create a secret and make a note of it

### 3. Assign the Monitoring Metrics Publisher role to the SP on the DCR
1. Go to your DCR resource in the Azure portal
2. Access Control (IAM) → Add role assignment
3. Select **Monitoring Metrics Publisher**
4. Assign to your service principal

### 4. Set environment variables
Set these in your terminal before running the script — never hardcode credentials:
```
set AZURE_TENANT_ID=your-tenant-id
set AZURE_CLIENT_ID=your-app-id
set AZURE_CLIENT_SECRET=your-client-secret
```

---

## How to run
```
python .txt-file-parsing.py --input logs.txt --dce YOUR_DCE_ENDPOINT --dcr YOUR_DCR_IMMUTABLE_ID --stream YOUR_STREAM_NAME
```

Example:
```
python .txt-file-parsing.py --input logs.txt --dce https://your-dce.eastus-1.ingest.monitor.azure.com --dcr dcr-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx --stream Custom-Json-CustomTableName_CL
```

---

## Arguments
| Argument   | Required | Description                                        |
|------------|----------|----------------------------------------------------|
| `--input`  | Yes      | Path to the input log .txt file                    |
| `--dce`    | Yes      | DCE endpoint URL                                   |
| `--dcr`    | Yes      | DCR immutable ID                                   |
| `--stream` | Yes      | DCR stream name                                    |

---

## Expected log format
Each line in the input file must follow this format:
```
YYYY-MM-DD HH:MM:SS LEVEL SOURCE MESSAGE
```
Example:
```
2026-03-31 08:12:04 INFO 192.168.1.1 System startup complete
2026-03-31 08:21:09 ERROR 192.168.1.99 Failed login attempt from unknown user
```

---

## Querying the data in Sentinel
Once ingested, query the custom table in your LAW Logs blade:
```
CustomTableName_CL
| order by TimeGenerated desc
```

---

## Known limitations
- The script ingests all records in the input file on every run — the LAW is append-only and does not deduplicate. In a production pipeline this would be handled by only pointing the script at new log files or tracking previously ingested records.
- Initial ingestion into a new table can take up to 15 minutes to appear in the LAW.

---

## Requirements
| Package          | Purpose                              |
|------------------|--------------------------------------|
| `azure-identity` | Service principal authentication     |
| `requests`       | HTTP POST to DCE endpoint            |
| `json`           | JSON serialisation (standard library)|
| `argparse`       | CLI argument parsing (standard library)|
| `os`             | Environment variable access (standard library)|
