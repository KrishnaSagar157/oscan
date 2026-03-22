import requests
import concurrent.futures
import random
import string

def get_random_path():
    return ''.join(random.choices(string.ascii_lowercase, k=10))

def directory_fuzz(domain):

    wordlist = ["admin", "login", "dashboard", "api", "backup", "dev"]

    found = []

    # Step 1: baseline request (fake path)
    fake_path = get_random_path()
    baseline_url = f"https://{domain}/{fake_path}"

    try:
        baseline = requests.get(baseline_url, timeout=3)
        baseline_len = len(baseline.text)
    except:
        baseline_len = 0

    def check(word):
        url = f"https://{domain}/{word}"

        try:
            r = requests.get(url, timeout=3)

            # Step 2: compare response size
            if r.status_code == 200 and abs(len(r.text) - baseline_len) > 50:
                return url

        except:
            return None

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(check, wordlist)

        for r in results:
            if r:
                found.append(r)

    return found
