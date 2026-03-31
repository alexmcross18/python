# .txt Log Parser

A Python script that parses plain text log files and outputs structured JSON data.

This project simulates the first stage of a custom log ingestion pipeline. In a production
environment the parsed output would be sent directly to an Azure Data Collection
Endpoint (DCE) via the Logs Ingestion API, rather than written to a file.

---

## What it does

- Reads a plain text log file (logs.txt)
- Parses each line into structured fields: date, time, level, source, and message
- Handles malformed or incomplete log lines without crashing
- Outputs the parsed data to a JSON file (parsed_logs.json)

---

## Files

| File               | Description                          |
|--------------------|--------------------------------------|
| .txt-file-parsing.py       | Main parser script                   |
| logs.txt           | Sample log file (input)              |
| parsed_logs.json   | Structured JSON output               |

---

## How to run

1. Make sure Python 3 is installed
2. Place logs.txt in the same folder as .txt-file-parsing.py
3. Run the script:

   python .txt-file-parsing.py

4. The parsed output will be saved to parsed_logs.json

---

## Expected log format

Each line in logs.txt should follow this format:

   YYYY-MM-DD HH:MM:SS LEVEL SOURCE MESSAGE

Example:

   2026-03-31 08:12:04 INFO 192.168.1.1 System startup complete
   2026-03-31 08:21:09 ERROR 192.168.1.99 Failed login attempt from unknown user

---

## Production context

In a real-world pipeline this script would be one part of a larger workflow:

1. Logs are collected automatically from network devices or servers
2. This script parses the raw logs into structured data
3. The structured data is sent to an Azure DCE endpoint via a HTTP POST request
4. Azure Monitor ingests the data into a Log Analytics Workspace/Sentinel for analysis

The parsed_logs.json file in this project mirrors the JSON payload that
would be sent to the DCE endpoint in step 3.

---

## Requirements

- Python 3
- No external libraries required (json is part of the Python standard library)
