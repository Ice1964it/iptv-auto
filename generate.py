import json
import urllib.request
from datetime import datetime

OUTPUT = "playlist.m3u"

SOURCE_URL = "https://raw.githubusercontent.com/ZapprTV/channels/refs/heads/main/it/dtt/national.json"

print("=== IPTV AUTO GENERATOR ===")

# scarica JSON
try:
    print("Downloading JSON...")
    with urllib.request.urlopen(SOURCE_URL) as response:
        data = json.loads(response.read().decode())

except Exception as e:
    print("DOWNLOAD ERROR:", e)
    exit(1)

channels = data.get("channels", []) if isinstance(data, dict) else data

print("TOTAL CHANNELS:", len(channels))


# ----------------------------
# FUNZIONI FILTRO
# ----------------------------

def get_valid_url(c):
    # 1. geoblock (priorità)
    geoblock = c.get("geoblock")
    if isinstance(geoblock, dict):
        gb_url = geoblock.get("url")
        if isinstance(gb_url, str) and ".m3u8" in gb_url:
            return gb_url

    # 2. url normale
    url = c.get("url")
    if isinstance(url, str) and ".m3u8" in url:
        return url

    return None


def is_supported(c, url):
    if not url:
        return False

    # solo HLS
    if c.get("type") != "hls":
        return False

    # blocca roba non compatibile con GSE IPTV
    bad = ["mpd", "widevine", "clearkey", "iframe", "zappr"]

    for b in bad:
        if b in url:
            return False

    return True


# ----------------------------
# FILTRO CANALI
# ----------------------------

valid = []

for c in channels:

    if not isinstance(c, dict):
        continue

    name = c.get("name")
    group = c.get("group", "TV")

    url = get_valid_url(c)

    if not name or not url:
        continue

    if not is_supported(c, url):
        continue

    valid.append({
        "name": name,
        "url": url,
        "group": group
    })

print("WORKING CHANNELS:", len(valid))


# ----------------------------
# CREA M3U
# ----------------------------

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

print("✅ FILE CREATED:", OUTPUT)
print("=== DONE ===")
