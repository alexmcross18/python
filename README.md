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

Folder: `scripts/deception-enrichment/`

---

### Log Parser — Log Analytics Workspace/Sentinel Pipeline
Parses plain text log files into structured JSON and ingests the data directly into
a Log Analytics Workspace/Sentinel custom table via an Azure Data Collection Endpoint
(DCE) and Data Collection Rule (DCR). Authenticates using a service principal via
environment variables — no stored credentials. Data lands in a custom table queryable
via KQL in Sentinel.

Folder: `scripts/log-parsing/`

---

## Structure
Each script lives in its own folder and follows the same structure:
```
script-name/
├── script.py        # main script
├── README.md        # what it does, how to run it, real world context
└── sample files     # any input/output examples
```

---

## Requirements
Each script lists its own dependencies in its README. In general:
- Python 3
- Some scripts require external libraries — install with pip as directed
- Some scripts require API keys or Azure credentials — these are always stored as
  environment variables and never hardcoded

---

## Notes
- Scripts are written to be readable and well commented — the goal is that
  anyone can follow the logic without needing to run the code
- More scripts will be added over time as new tools and workflows are built out
