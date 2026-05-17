import json
import os
from datetime import datetime

OUTPUT = "playlist.m3u"

print("=== IPTV DEBUG START ===")

# 1. mostra file presenti
print("FILES IN REPO:")
print(os.listdir())

# 2. verifica file JSON
if not os.path.exists("channels.json"):
    print("ERROR: channels.json NOT FOUND")
    exit(1)

# 3. carica JSON in modo sicuro
try:
    with open("channels.json", "r", encoding="utf-8") as f:
        raw = f.read()
        print("\nJSON RAW SIZE:", len(raw))

        channels = json.loads(raw)

except Exception as e:
    print("ERROR READING JSON:", e)
    exit(1)

print("\nCHANNEL COUNT:", len(channels))

valid = []

for c in channels:

    print("CHECK:", c)

    name = c.get("name")
    group = c.get("group")
    url = c.get("url")

    if not name or not group or not url:
        print("SKIP INVALID:", c)
        continue

    valid.append(c)

print("\nVALID CHANNELS:", len(valid))

# 4. FORZA SCRITTURA FILE (anche se vuoto)
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
    print("⚠️ WARNING: playlist empty -> JSON problem or file not loaded")

print("=== IPTV DEBUG END ===")
