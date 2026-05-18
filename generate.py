import json
import urllib.request
from datetime import datetime

OUTPUT = "playlist.m3u"

SOURCE_URL = "https://raw.githubusercontent.com/ZapprTV/channels/refs/heads/main/it/dtt/national.json"

def get_url(c):
    # priorità geoblock
    gb = c.get("geoblock")
    if isinstance(gb, dict):
        u = gb.get("url")
        if isinstance(u, str) and ".m3u8" in u:
            return u

    u = c.get("url")
    if isinstance(u, str) and ".m3u8" in u:
        return u

    return None


def is_ok(c, url):
    if not url:
        return False

    if c.get("type") != "hls":
        return False

    bad = ["mpd", "widevine", "clearkey", "iframe", "zappr"]

    for b in bad:
        if b in url:
            return False

    return True


print("Generating playlist...")

with urllib.request.urlopen(SOURCE_URL) as r:
    data = json.loads(r.read().decode())

channels = data.get("channels", []) if isinstance(data, dict) else data

valid = []

for c in channels:
    if not isinstance(c, dict):
        continue

    name = c.get("name")
    url = get_url(c)

    if not name or not url:
        continue

    if not is_ok(c, url):
        continue

    valid.append((name, url))

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")
    f.write(f"# Updated {datetime.now()}\n\n")

    for name, url in valid:
        f.write(f"#EXTINF:-1,{name}\n")
        f.write(url + "\n")

print("Done:", len(valid), "channels")
