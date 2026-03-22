import requests

def header_analysis(domain):

    url = f"https://{domain}"

    try:
        response = requests.get(url, timeout=5)

        headers = response.headers

        security_headers = {
            "Strict-Transport-Security": headers.get("Strict-Transport-Security"),
            "Content-Security-Policy": headers.get("Content-Security-Policy"),
            "X-Frame-Options": headers.get("X-Frame-Options"),
            "X-Content-Type-Options": headers.get("X-Content-Type-Options"),
            "Referrer-Policy": headers.get("Referrer-Policy")
        }

        return headers, security_headers

    except Exception as e:
        return {"error": str(e)}, {}
