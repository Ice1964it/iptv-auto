import json
from datetime import datetime

OUTPUT = "playlist.m3u"

with open("channels.json", "r", encoding="utf-8") as f:
    channels = json.load(f)

channels = sorted(channels, key=lambda x: (x["group"], x["name"]))

print("\nGenerating playlist...\n")

with open(OUTPUT, "w", encoding="utf-8") as f:

    f.write("#EXTM3U\n")
    f.write(f"# Generated: {datetime.now()}\n\n")

    current_group = ""

    for c in channels:

        if c["group"] != current_group:
            current_group = c["group"]
            f.write(f"\n# ===== {current_group} =====\n\n")

        print(f"ADD {c['name']}")

        f.write(
            f'#EXTINF:-1 group-title="{c["group"]}",{c["name"]}\n'
        )
        f.write(c["url"] + "\n")

print("\nDONE")
print("Channels:", len(channels))
