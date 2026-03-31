# AbuseIPDB IP Enrichment Script

A Python script that reads IP addresses from a CSV file, looks each one up against
the AbuseIPDB threat intelligence API, and writes an enriched report sorted by abuse
confidence score — highest risk IPs first.

---

## Real world use case

When a decoy asset in Zscaler Deception is triggered, the IOCs seen by that host can
be exported as a CSV. This script enriches those IPs against AbuseIPDB to identify
which ones are known malicious infrastructure, so confirmed bad IPs can be passed to
the SOC for a threat hunt across the environment.

---

## Files

| File            | Description                         |
|-----------------|-------------------------------------|
| enrich.py       | Main enrichment script              |
| alerts.csv      | Sample input file (IP addresses)    |
| enrichment.txt  | Enriched output report              |

---

## Requirements

Python 3 and the requests library installed:

   pip install requests

---

## API key setup

The API key is read from a Windows environment variable — it is never stored in the code.

1. Sign up for a free account at https://www.abuseipdb.com/register
2. Go to https://www.abuseipdb.com/account/api - create and copy your key
3. Create a new environment variable and call it "AbuseIP"

---

## Usage

1. Export your IOCs from Zscaler Deception as a CSV
2. Place the CSV in the same folder as the script
3. Update the settings at the top of the script if needed:

   INPUT_FILE  = "alerts.csv"    # your CSV filename
   IP_COLUMN   = "IPAddress"     # the column containing IP addresses
   OUTPUT_FILE = "enrichment.txt"

4. Run the script:

   python enrich.py

---

## Output

Results are written to enrichment.txt, sorted by abuse confidence score with the
highest risk IPs at the top. Any IP scoring above 20 is flagged:

   ─────────────────────────────────
   IP Address:        185.220.101.45
   Confidence Score:  100 / 100
   Total Reports:     782
   Country:           DE
   Usage Type:        tor
   ISP:               Frantech Solutions
   Is Whitelisted:    False
   Last Reported:     2026-03-28T09:12:00+00:00

   ⚠ FLAGGED - SCORE ABOVE 20
   ─────────────────────────────────
   IP Address:        198.199.119.161
   Confidence Score:  0 / 100
   Total Reports:     0

---

## Notes

- The output file uses "x" mode — it will not overwrite an existing enrichment file.
  This is intentional so that if this script is run on a schedule, previous results
  are preserved until an analyst has had the chance to review and action them. Rename
  or move the previous enrichment.txt before each run.

- Duplicate IPs in the input CSV are deduplicated automatically — the API is only
  called once per unique IP.

- The script pauses 1.5 seconds between API calls to stay within AbuseIPDB's free
  tier rate limit of 1000 requests per day.

- A confidence score of 0 does not necessarily mean an IP is safe — newly provisioned
  attacker infrastructure may not have been reported yet. Any IP that contacted your
  decoy asset should be treated as suspicious regardless of score.

---

## Limitations

- AbuseIPDB only reflects what has been reported — unknown or newly stood-up
  infrastructure will score 0 even if malicious.

- The free tier allows 1000 requests per day — large IP lists may hit this limit.

- Results reflect a point-in-time snapshot and should be re-run if the hunt
  is delayed by more than a few days.
