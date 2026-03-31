# Python

A collection of Python scripts built around security operations and automation.
Each script has its own folder with a README explaining what it does, how to run
it, and how it fits into a real-world workflow.

---

## Scripts

### AbuseIPDB IP Enrichment
Reads IP addresses from a CSV file, queries the AbuseIPDB threat intelligence API,
and outputs an enriched report sorted by abuse confidence score. Built around a
Zscaler Deception workflow where IOCs from a triggered decoy are passed to the SOC
for a threat hunt.

Folder: scripts/deception-enrichment/

---

### Log Parser
Parses plain text log files into structured JSON data. Simulates the first stage
of a log ingestion pipeline — in production the parsed output would be sent directly
to an Azure Data Collection Endpoint (DCE) via the Logs Ingestion API.

Folder: scripts/log-parsing/

---

## Structure

Each script lives in its own folder and follows the same structure:
```
script-name/
├── script.py        # main script
├── README.md        # what it does, how to run it, real world context
└── sample files     # any input/output examples
```

## Requirements

Each script lists its own dependencies in its README. In general:

- Python 3
- Some scripts require external libraries — install with pip as directed
- Some scripts require API keys — these are always stored as environment
  variables and never hardcoded

---

## Notes

- Scripts are written to be readable and well commented — the goal is that
  anyone can follow the logic without needing to run the code
- More scripts will be added over time as new tools and workflows are built out
****
