"""One-off diagnostic: not part of the pipeline. Fetches each problem URL from
a real internet connection (this sandbox's own network is restricted; GitHub
Actions runners are not) and prints enough structure to write correct
selectors - status code, final URL after redirects, title, and any class
names that mention "event". Delete this file and its workflow once the
selectors in config/local_sources.yml are fixed.
"""
import re

import requests

HEADERS = {"User-Agent": "seattle-events-monitor/1.0 (personal project, contact via github)"}

url = "https://mohai.org/events/"
resp = requests.get(url, headers=HEADERS, timeout=20)
print(f"status={resp.status_code} length={len(resp.text)}")

idx = resp.text.find("tribe-events-calendar-list__event-row")
if idx == -1:
    print("no event-row class found - dumping first 3000 chars instead")
    print(resp.text[:3000])
else:
    print("--- snippet around first event row ---")
    print(resp.text[max(0, idx - 200):idx + 2500])

