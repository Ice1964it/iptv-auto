import json
import os
from datetime import datetime

OUTPUT = "playlist.m3u"

print("=== IPTV DEBUG START ===")

print("FILES IN REPO:")
print(os.listdir())

if not os.path.exists("channels.json"):
    print("ERROR: channels.json NOT FOUND")
    exit(1)

try:
    with open("channels.json", "r", encoding="utf-8") as f:
        raw = f.read()
        print("\nJSON RAW SIZE:", len(raw))

        data = json.loads(raw)

        if isinstance(data, dict):
            channels = data.get("channels", [])
        else:
            channels = data

except Exception as e:
    print("ERROR READING JSON:", e)
    exit(1)

print("\nCHANNEL COUNT:", len(channels))

valid = []

for c in channels:

    print("CHECK:", c.get("name"))

    if not isinstance(c, dict):
        print("SKIP NON-DICT:", c)
        continue

    name = c.get("name")
    group = c.get("group", "TV")

    # 🔥 LOGICA URL CORRETTA
    url = None

    # 1. usa geoblock se disponibile
    geoblock = c.get("geoblock")
    if isinstance(geoblock, dict):
        gb_url = geoblock.get("url")
        if isinstance(gb_url, str) and gb_url.startswith("http"):
            url = gb_url
            print("USE GEOBLOCK")

    # 2. fallback su url normale
    if not url:
        raw_url = c.get("url")
        if isinstance(raw_url, str) and raw_url.startswith("http"):
            url = raw_url

    # 3. scarta se niente
    if not name or not url:
        print("SKIP INVALID:", c.get("name"))
        continue

    # 4. solo HLS (evita DRM / DASH / iframe / zappr)
    if c.get("type") != "hls":
        print("SKIP NON HLS:", c.get("type"))
        continue
        
    if "akamai" in url or "zappr" in url:
        pass  # ok
    elif "cloudfront" in url:
        print("SKIP DRM POSSIBILE:", url)
        continue
        
    valid.append({
        "name": name,
        "url": url,
        "group": group
    })

print("\nVALID CHANNELS:", len(valid))

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

print("\nFILE WRITTEN:", OUTPUT)

if len(valid) == 0:
    print("⚠️ WARNING: playlist empty")

print("=== IPTV DEBUG END ===")
