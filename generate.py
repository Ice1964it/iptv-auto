import json
from datetime import datetime

OUTPUT = "playlist.m3u"

with open("channels.json", "r", encoding="utf-8") as f:
    channels = json.load(f)

online = []

print("Generating playlist...\n")

for c in channels:
    print(f"ADD  {c['name']}")
    online.append(c)

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(f"# Generated: {datetime.now().isoformat()}\n")
    f.write("#EXTM3U\n")

    for c in online:
        f.write(f'#EXTINF:-1 group-title="{c["group"]}",{c["name"]}\n')
        f.write(c["url"] + "\n")

print("\nPlaylist generated.")
print("Channels:", len(online))
