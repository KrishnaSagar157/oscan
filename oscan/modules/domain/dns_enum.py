import subprocess

def dns_enumeration(domain):

    records = {}

    queries = {
        "A": ["dig", domain, "A", "+short"],
        "MX": ["dig", domain, "MX", "+short"],
        "NS": ["dig", domain, "NS", "+short"],
        "TXT": ["dig", domain, "TXT", "+short"]
    }

    for record_type, command in queries.items():

        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        records[record_type] = result.stdout.strip()

    return records
