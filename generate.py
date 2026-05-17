import json
from datetime import datetime

OUTPUT = "playlist.m3u"

print("Loading channels.json...")

with open("channels.json", "r", encoding="utf-8") as f:
    channels = json.load(f)

print("Generating playlist...\n")

valid = []

for c in channels:

    name = c.get("name")
    group = c.get("group")
    url = c.get("url")

    # sicurezza totale
    if not name or not group or not url:
        print("SKIP invalid channel:", c)
        continue

    valid.append(c)

with open(OUTPUT, "w", encoding="utf-8") as f:

    f.write("#EXTM3U\n")
    f.write(f"# Generated: {datetime.now()}\n\n")

    current_group = ""

    for c in valid:

        if c["group"] != current_group:
            current_group = c["group"]
            f.write(f"\n# ===== {current_group} =====\n\n")

        print("ADD", c["name"])

        f.write(f'#EXTINF:-1 group-title="{c["group"]}",{c["name"]}\n')
        f.write(c["url"] + "\n")

print("\nDONE")
print("Valid channels:", len(valid))
print("Skipped channels:", len(channels) - len(valid))
