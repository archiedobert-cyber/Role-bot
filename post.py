import os
import requests

# ---- Set your message here ----
MESSAGE = "Your hourly message here"
# --------------------------------

# Reads every environment variable that starts with WEBHOOK_
# so you can add as many channels as you like without touching this file.
webhook_urls = [v for k, v in os.environ.items() if k.startswith("WEBHOOK_")]

if not webhook_urls:
    raise SystemExit("No WEBHOOK_* environment variables found. Check your repo secrets and workflow file.")

failures = []

for url in webhook_urls:
    response = requests.post(url, json={"content": MESSAGE})
    if response.status_code not in (200, 204):
        failures.append((url, response.status_code, response.text))
        print(f"Failed to post: {response.status_code} {response.text}")
    else:
        print("Posted successfully to one channel.")

if failures:
    raise SystemExit(f"{len(failures)} of {len(webhook_urls)} posts failed.")
