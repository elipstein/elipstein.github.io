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

URLS = [
    "https://www.elliottbaybook.com/events",
    "https://www.thirdplacebooks.com/events",
    "https://ubookstore.com/events",
    "https://www.ubookstore.com/pages/events",
    "https://mohai.org/events/",
]

for url in URLS:
    print(f"\n=== {url} ===")
    try:
        resp = requests.get(url, headers=HEADERS, timeout=20, allow_redirects=True)
    except requests.RequestException as exc:
        print(f"REQUEST FAILED: {exc}")
        continue
    print(f"status={resp.status_code} final_url={resp.url} length={len(resp.text)}")
    title_match = re.search(r"<title[^>]*>(.*?)</title>", resp.text, re.IGNORECASE | re.DOTALL)
    print(f"title={title_match.group(1).strip() if title_match else 'NONE'}")
    classes = set(re.findall(r'class="([^"]*event[^"]*)"', resp.text, re.IGNORECASE))
    print(f"classes containing 'event' ({len(classes)}):")
    for c in sorted(classes)[:25]:
        print(f"  {c}")
    if resp.status_code == 403 or not classes:
        snippet = resp.text[:1500].replace("\n", " ")
        print(f"snippet: {snippet}")
