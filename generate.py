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

with open("channels.json", "r", encoding="utf-8") as f:
    channels = json.load(f)

final = []

print("\nChecking with fallback system...\n")

for c in channels:

    working = None

    for url in c["sources"]:
        if check(url):
            working = url
            break

    if working:
        print(f"OK   {c['name']}")
        final.append({
            "name": c["name"],
            "group": c["group"],
            "url": working
        })
    else:
        print(f"OFF  {c['name']}")

final.sort(key=lambda x: (x["group"], x["name"]))

with open(OUTPUT, "w", encoding="utf-8") as f:

    f.write("#EXTM3U\n")
    f.write(f"# AUTO HEAL IPTV {datetime.now()}\n\n")

    group = ""

    for c in final:

        if c["group"] != group:
            group = c["group"]
            f.write(f"\n# ===== {group} =====\n\n")

        f.write(f'#EXTINF:-1 group-title="{c["group"]}",{c["name"]}\n')
        f.write(c["url"] + "\n")

print("\nDONE:", len(final))
