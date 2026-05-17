import json
from datetime import datetime

OUTPUT = "playlist.m3u"

# Carica canali
with open("channels.json", "r", encoding="utf-8") as f:
    channels = json.load(f)

print("Generating playlist...")

# Scrive playlist
with open(OUTPUT, "w", encoding="utf-8") as f:

    f.write("#EXTM3U\n")
    f.write(f"# Generated: {datetime.now()}\n\n")

    for c in channels:

        print(f"ADD {c['name']}")

        f.write(
            f'#EXTINF:-1 group-title="{c["group"]}",{c["name"]}\n'
        )

        f.write(c["url"] + "\n")

print("Playlist generated.")
print("Channels:", len(channels))
