import os
from datetime import datetime
# ---------------- USERNAME ----------------#
def generate_report(username, sherlock_data, maigret_data, scan_time):
    scan_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs("reports/username", exist_ok=True)

    platforms = {}

    # --- Sherlock parsing --- #
    for line in sherlock_data.splitlines():
        if "[+]" in line:
            platform = line.split(":")[0].replace("[+]", "").strip()
            platforms.setdefault(platform, []).append("Sherlock")

    # --- Maigret parsing --- #
    for line in maigret_data.splitlines():
        if "[+]" in line:
            platform = line.split(":")[0].replace("[+]", "").strip()
            platforms.setdefault(platform, []).append("Maigret")

    accounts_found = len(platforms)

    filename = f"reports/username/{username}.txt"

    with open(filename, "w") as file:

        file.write("OSINT Username Investigation Report\n")
        file.write("="*40 + "\n\n")

        file.write(f"Username: {username}\n")
        file.write(f"Accounts Found: {accounts_found}\n")
        file.write(f"Scan Time: {scan_time} seconds\n\n")
        file.write(f"Scanned At: {scan_timestamp}\n\n")

        file.write("Platforms Found:\n")

        for platform, tools in platforms.items():
            file.write(f"{platform} ({', '.join(tools)})\n")

        file.write("\n--- SHERLOCK RAW OUTPUT ---\n\n")
        file.write(sherlock_data)

        file.write("\n\n--- MAIGRET RAW OUTPUT ---\n\n")
        file.write(maigret_data)

    print(f"[+] Report saved to {filename}")

# ---------------- DOMAIN --------------- #
def save_domain_report(domain, dns, subs, headers, security, dirs, ports, scan_time):
    scan_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs("reports/domain", exist_ok=True)

    filename = os.path.join("reports", "domain", f"{domain}.txt")

    with open(filename, "w") as f:

        f.write("OSCAN DOMAIN REPORT\n")
        f.write("="*50 + "\n\n")

        f.write(f"Target: {domain}\n\n")

        # DNS
        f.write("[ DNS ENUMERATION ]\n")
        f.write("-"*30 + "\n")
        for k, v in dns.items():
            f.write(f"{k}: {v}\n")
        f.write("\n")

        # Subdomains
        f.write("[ SUBDOMAINS ]\n")
        f.write("-"*30 + "\n")
        for s in subs:
            f.write(s + "\n")
        f.write("\n")

        # Headers
        f.write("[ HTTP HEADERS ]\n")
        f.write("-"*30 + "\n")
        for k, v in headers.items():
            f.write(f"{k}: {v}\n")
        f.write("\n")

        # Security
        f.write("[ SECURITY ANALYSIS ]\n")
        f.write("-"*30 + "\n")
        for k, v in security.items():
            status = "Present" if v else "Missing"
            f.write(f"{k}: {status}\n")
        f.write("\n")

        # Directories
        f.write("[ DIRECTORIES ]\n")
        f.write("-"*30 + "\n")
        for d in dirs:
            f.write(d + "\n")
        f.write("\n")

        # Ports
        f.write("[ OPEN PORTS ]\n")
        f.write("-"*30 + "\n")
        for p in ports:
            f.write(str(p) + "\n")
        
        file.write(f"Scan Time: {scan_time} seconds\n")
        file.write(f"Scanned At: {scan_timestamp}\n\n")
    
    print(f"[+] Report saved: {filename}")
