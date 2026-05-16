import json
import requests
from datetime import datetime

OUTPUT = "playlist.m3u"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def check(url):
    try:
        r = requests.get(url, timeout=10, headers=HEADERS)
        return r.status_code == 200
    except:
        return False

with open("channels.json", "r") as f:
    channels = json.load(f)

online = []

print("Checking streams...\n")

for c in channels:
    status = check(c["url"])

    if status:
        print(f"OK   {c['name']}")
        online.append(c)
    else:
        print(f"OFF  {c['name']}")

with open(OUTPUT, "w", encoding="utf-8") as f:

    f.write("#EXTM3U\n")

    for c in online:

        f.write(
            f'#EXTINF:-1 group-title="{c["group"]}",{c["name"]}\n'
        )

        f.write(c["url"] + "\n")

print("\nPlaylist generated.")
print("Channels:", len(online))
print("Date:", datetime.now())