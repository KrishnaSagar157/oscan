import requests

def subdomain_enum(domain):

    url = f"https://crt.sh/?q=%25.{domain}&output=json"

    response = requests.get(url)

    subdomains = set()

    if response.status_code == 200:

        data = response.json()

        for entry in data:

            name = entry.get("name_value")

            if name:
                for sub in name.split("\n"):
                    if domain in sub:
                        subdomains.add(sub.strip())

    return sorted(subdomains)
