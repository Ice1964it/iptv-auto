import json
import requests
from datetime import datetime

OUTPUT = "playlist.m3u"

HEADERS = {"User-Agent": "Mozilla/5.0"}

def check(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=6, allow_redirects=True, stream=True)
        return r.status_code < 400
    except:
        return False

print("Loading channels.json...")

with open("channels.json", "r", encoding="utf-8") as f:
    channels = json.load(f)

valid = []

print("\nChecking sources...\n")

for c in channels:

    name = c.get("name")
    group = c.get("group")
    sources = c.get("sources", [])

    if not name or not group or not sources:
        print("SKIP invalid:", c)
        continue

    working_url = None

    for url in sources:
        if check(url):
            working_url = url
            break

    if working_url:
        print("OK  ", name)
        valid.append({
            "name": name,
            "group": group,
            "url": working_url
        })
    else:
        print("OFF ", name)

with open(OUTPUT, "w", encoding="utf-8") as f:

    f.write("#EXTM3U\n")
    f.write(f"# Generated: {datetime.now()}\n\n")

    current_group = ""

    for c in valid:

        if c["group"] != current_group:
            current_group = c["group"]
            f.write(f"\n# ===== {current_group} =====\n\n")

        f.write(f'#EXTINF:-1 group-title="{c["group"]}",{c["name"]}\n')
        f.write(c["url"] + "\n")

print("\nDONE")
print("Valid:", len(valid))
print("Total:", len(channels))
