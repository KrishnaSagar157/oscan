import shutil
import subprocess

def search_maigret(username):

    # --- Check if maigret exists --- #
    if not shutil.which("maigret"):
        return "[!] Maigret not found. Install: pipx install maigret"

    command = ["maigret", username, "--no-progressbar"]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    return result.stdout + result.stderr
