import argparse
import concurrent.futures
import time

from oscan.modules.username.sherlock_search import search_sherlock
from oscan.modules.username.maigret_search import search_maigret

from oscan.modules.domain.dns_enum import dns_enumeration
from oscan.modules.domain.subdomain_enum import subdomain_enum

from oscan.modules.web.header_analysis import header_analysis
from oscan.modules.web.dir_fuzz import directory_fuzz

from oscan.modules.network.port_scan import port_scan

from oscan.report_generator import generate_report, save_domain_report

from colorama import Fore, Style, init
init(autoreset=True)
# ---------------- FUNCTIONS ---------------- #

def get_risk(header, present):

    if present:
        return "LOW"

    high_risk = [
        "Content-Security-Policy",
        "Strict-Transport-Security"
    ]

    medium_risk = [
        "X-Frame-Options",
        "X-Content-Type-Options"
    ]

    low_risk = [
        "Referrer-Policy",
        "X-XSS-Protection"
    ]

    if header in high_risk:
        return "HIGH"
    elif header in medium_risk:
        return "MEDIUM"
    elif header in low_risk:
        return "LOW"
    else:
        return "UNKNOWN"

def color_risk(risk):

    if risk == "HIGH":
        return Fore.RED
    elif risk == "MEDIUM":
        return Fore.YELLOW
    else:
        return Fore.GREEN

def get_explanation(header, present):

    if present:
        return "Properly configured"

    explanations = {
        "Content-Security-Policy": "allows XSS attacks",
        "Strict-Transport-Security": "connection can be downgraded to HTTP (MITM risk)",
        "X-Frame-Options": "site vulnerable to clickjacking",
        "X-Content-Type-Options": "browser may misinterpret content (MIME sniffing)",
        "Referrer-Policy": "may leak sensitive URL data",
        "X-XSS-Protection": "legacy protection missing (low impact)"
    }

    return explanations.get(header, "no description available")

# ---------------- SCORING ----------------#

def calculate_score(security, ports, directories):

    score = 100

    # -------- HEADERS -------- #
    for header, present in security.items():

        if present:
            continue

        if header == "Content-Security-Policy":
            score -= 25

        elif header == "Strict-Transport-Security":
            score -= 20

        elif header in ["X-Frame-Options", "X-Content-Type-Options"]:
            score -= 10

        elif header in ["Referrer-Policy", "X-XSS-Protection"]:
            score -= 5

    # -------- PORTS -------- #
    risky_ports = [21, 23, 25, 110, 143, 3306]

    for p in ports:
        if p in risky_ports:
            score -= 15   # dangerous exposed service

    # -------- DIRECTORIES -------- #
    sensitive_keywords = ["admin", "login", "dashboard"]

    for d in directories:
        for keyword in sensitive_keywords:
            if keyword in d.lower():
                score -= 5

    return max(score, 0)

# ---------------- ARGUMENT PARSER ---------------- #

parser = argparse.ArgumentParser(
    description="OSCAN - Automated OSINT Recon Tool"
)

parser.add_argument(
    "type",
    choices=["username", "domain"],
    help="Type of scan (username or domain)"
)

parser.add_argument(
    "target",
    help="Target username or domain"
)

parser.add_argument(
    "--quiet",
    action="store_true",
    help="Run silently, only save report"
)

args = parser.parse_args()
target = args.target
scan_type = args.type
quiet = args.quiet
# ---------------- MAIN ----------------#
def main():
    # ---------------- USERNAME ---------------- #

    if args.type == "username":

        print(f"[+] Scanning username: {args.target}")

        with concurrent.futures.ThreadPoolExecutor() as executor:

            sherlock_future = executor.submit(search_sherlock, args.target)
            maigret_future = executor.submit(search_maigret, args.target)

            sherlock_results, scan_time = sherlock_future.result()
            maigret_results = maigret_future.result()

        generate_report(args.target, sherlock_results, maigret_results, scan_time)


    # ---------------- DOMAIN ---------------- #

    elif scan_type == "domain":

        if not quiet:
            print(f"{Fore.GREEN}[+] Running domain recon on: {target}{Style.RESET_ALL}")

        start_time = time.time()
        # Run scans
        dns_results = dns_enumeration(target)
        subdomains = subdomain_enum(target)
        headers, security = header_analysis(target)
        directories = directory_fuzz(target)
        ports = port_scan(target)

        scan_time = round(time.time() - start_time, 2)
        if not quiet:

            # ---------------- DNS ---------------- #
            print(f"{Fore.CYAN}\n--- DNS ---{Style.RESET_ALL}")

            for record, value in dns_results.items():

                print(f"{Fore.YELLOW}{record}:{Style.RESET_ALL}")

                if value:
                    for line in value.split("\n"):
                        print(f"  {line}")
                else:
                    print("  No data")

            # ---------------- SUBDOMAINS ---------------- #
            print(f"{Fore.CYAN}\n--- Subdomains ---{Style.RESET_ALL}")

            for s in subdomains:
                if "*" not in s:   # skip wildcard
                    print(s)

            # ---------------- HEADERS ---------------- #
            print(f"{Fore.CYAN}\n--- Headers ---{Style.RESET_ALL}")

            for k, v in headers.items():
                print(f"{k}: {v}")

            # ---------------- SECURITY ---------------- #
            print(f"{Fore.CYAN}\n--- SECURITY ANALYSIS ---{Style.RESET_ALL}")

            for k, v in security.items():

                risk = get_risk(k, v)
                color = color_risk(risk)

                status = "Present" if v else "Missing"

                explanation = get_explanation(k, v)

                print(f"{color}[{risk}] {k}: {status} {Style.DIM}→ {explanation}{Style.RESET_ALL}")
        
            # ---------------- DIRECTORIES ---------------- #
            print(f"{Fore.CYAN}\n--- Directories ---{Style.RESET_ALL}")

            for d in directories:
                print(d)

            # ---------------- PORTS ---------------- #
            print(f"{Fore.CYAN}\n--- Open Ports ---{Style.RESET_ALL}")

            for p in ports:
                print(f"{Fore.YELLOW}{p}{Style.RESET_ALL}")

            # ---------------- SCORING ----------------#
            score = calculate_score(security, ports, directories)

            print(f"\n{Fore.CYAN}--- SECURITY SCORE ---{Style.RESET_ALL}")

            if score >= 80:
                level = "SECURE"
            elif score >= 50:
                level = "MODERATE"
            else:
                level = "WEAK"

            print(f"{color}{level} ({score}/10) {Style.RESET_ALL}")    

        # Save report
        save_domain_report(target, dns_results, subdomains, headers, security, directories, ports, scan_time)
if __name__ == "__main__":
    main()
