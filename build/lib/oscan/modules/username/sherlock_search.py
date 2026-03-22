import subprocess
import time

def search_sherlock(username):
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
