# OSCAN – Automated OSINT Recon Tool

OSCAN is a CLI-based tool that automates reconnaissance tasks such as domain analysis and username enumeration, with built-in security analysis and scoring.

---

## Features

### Username Enumeration

* Searches usernames across platforms using Sherlock and Maigret
* Parallel scanning for faster results
* Consolidated reporting

---

### Domain Reconnaissance

* DNS Enumeration (A, MX, NS, TXT)
* Subdomain Discovery (crt.sh)
* HTTP Header Analysis
* Directory Fuzzing
* Port Scanning (multi-threaded)

---

### Security Analysis

* Detects missing security headers
* Risk classification (HIGH / MEDIUM / LOW)
* Provides explanation for each issue

Example:

```
[HIGH] Content-Security-Policy: Missing → allows XSS attacks
```

---

### Security Scoring

* Score starts at 100
* Deducts based on severity
* Considers ports and sensitive directories

Example:

```
MODERATE (65/100)
```

---

## Installation

### Using pipx (Recommended)

```
pipx install .
```

---

## Usage

### Domain Scan

```
oscan domain example.com
```

### Username Scan

```
oscan username johndoe
```

---

## Reports

Reports are automatically generated in:

```
./reports/
```

* reports/domain/
* reports/username/

---

## Tech Stack

* Python
* requests
* socket
* concurrent.futures
* argparse
* colorama

---

## Additional Requirements

This tool depends on external OSINT tools:

* Sherlock
* Maigret

Install them before using OSCAN:

```bash
pipx install sherlock-project
pipx install maigret
```

## Why OSCAN

* Combines multiple reconnaissance techniques into one tool
* Performs analysis and scoring, not just data collection
* Designed to be simple to use and informative

---

## Disclaimer

This tool is intended for educational and ethical use only.
Do not use it on systems without proper authorization.

---

## Author

K S
