import json
import os
from datetime import datetime

OUTPUT = "playlist.m3u"

def get_valid_url(c):
    url = None

    # 1. geoblock (priorità)
    geoblock = c.get("geoblock")
    if isinstance(geoblock, dict):
        gb_url = geoblock.get("url")
        if isinstance(gb_url, str) and gb_url.startswith("http") and ".m3u8" in gb_url:
            return gb_url

    # 2. url normale
    raw_url = c.get("url")
    if isinstance(raw_url, str) and raw_url.startswith("http") and ".m3u8" in raw_url:
        url = raw_url

    return url


def is_working_channel(c, url):
    if not url:
        return False

    # solo HLS
    if c.get("type") != "hls":
        return False

    # scarta DRM / roba problematica
    bad_keywords = [
        "cloudfront",   # spesso DRM
        "mpd",          # dash
        "widevine",
        "clearkey"
    ]

    for k in bad_keywords:
        if k in url:
            return False

    # scarta url strane
    if not url.startswith("http"):
        return False

    return True


print("=== IPTV FILTER START ===")

if not os.path.exists("channels.json"):
    print("channels.json NOT FOUND")
    exit(1)

with open("channels.json", "r", encoding="utf-8") as f:
    data = json.load(f)

channels = data.get("channels", []) if isinstance(data, dict) else data

print("TOTAL CHANNELS:", len(channels))

valid = []

for c in channels:

    if not isinstance(c, dict):
        continue

    name = c.get("name")
    group = c.get("group", "TV")

    url = get_valid_url(c)

    if not name or not url:
        continue

    if not is_working_channel(c, url):
        continue

    valid.append({
        "name": name,
        "url": url,
        "group": group
    })

print("WORKING CHANNELS:", len(valid))


# scrittura M3U
with open(OUTPUT, "w", encoding="utf-8") as f:

    f.write("#EXTM3U\n")
    f.write(f"# Generated {datetime.now()}\n\n")

    current = ""

    for c in valid:

        if c["group"] != current:
            current = c["group"]
            f.write(f"\n# ===== {current} =====\n\n")

        f.write(f'#EXTINF:-1 group-title="{c["group"]}",{c["name"]}\n')
        f.write(c["url"] + "\n")

print("FILE CREATED:", OUTPUT)
print("=== IPTV FILTER END ===")
