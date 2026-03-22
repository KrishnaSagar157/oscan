import subprocess
import time
import shutil

def search_sherlock(username):
    # --- Check if sherlock exists ---#
    if not shutil.which("sherlock"):
        return "[!] Sherlock not found. Install: pipx install sherlock-project"

    command=["sherlock", username, "--print-found", "--no-txt"]
    start_time = time.time()

    result = subprocess.run(
        command,
	capture_output=True,
	text=True
        )
    end_time = time.time()
    scan_time = round(end_time - start_time, 2)
    return result.stdout, scan_time
