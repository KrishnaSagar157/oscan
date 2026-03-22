import subprocess

def search_maigret(username):

    command = ["maigret", username, "--no-progressbar"]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    return result.stdout + result.stderr

