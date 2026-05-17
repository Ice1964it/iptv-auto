import json
from datetime import datetime

OUTPUT = "playlist.m3u"

print("Loading channels.json...")

with open("channels.json", "r", encoding="utf-8") as f:
    channels = json.load(f)

valid = []

print("\nBuilding playlist (no strict filtering)...\n")

for c in channels:

    name = c.get("name")
    group = c.get("group")
    sources = c.get("sources", [])

    # fallback: se sources vuoto NON bloccare tutto
    if not name or not group:
        print("SKIP invalid entry:", c)
        continue

    # prende primo source disponibile
    url = None

    if isinstance(sources, list) and len(sources) > 0:
        url = sources[0]

    if not url:
        print("SKIP no url:", name)
        continue

    print("ADD", name)

    valid.append({
        "name": name,
        "group": group,
        "url": url
    })

# 🔥 FORZARE CREAZIONE FILE SEMPRE
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

# 🔥 DEBUG OBBLIGATORIO
print("\nDONE")
print("Channels in JSON:", len(channels))
print("Channels written:", len(valid))

if len(valid) == 0:
    print("\nWARNING: playlist EMPTY -> problem in sources")
