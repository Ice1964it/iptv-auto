import json
from datetime import datetime

OUTPUT = "playlist.m3u"
README = "README.md"

EPG_URL = "https://epgshare01.online/epgshare01/epg_ripper_IT1.xml.gz"

LOGOS = {
    "Rai News 24": "https://upload.wikimedia.org/wikipedia/commons/d/d0/RaiNews24.svg",
    "Rai 3": "https://upload.wikimedia.org/wikipedia/commons/5/5a/Rai_3_-_Logo_2016.svg",
    "Canale 5": "https://upload.wikimedia.org/wikipedia/commons/0/0a/Canale_5_-_2018.svg",
    "Italia 1": "https://upload.wikimedia.org/wikipedia/commons/f/f6/Italia1.svg",
    "Rete 4": "https://upload.wikimedia.org/wikipedia/commons/3/37/Rete_4_-_2018.svg",
    "TV8": "https://upload.wikimedia.org/wikipedia/commons/3/38/TV8_logo.svg",
    "La7": "https://upload.wikimedia.org/wikipedia/commons/0/02/LA7_-_Logo_2011.svg"
}

with open("channels.json", "r", encoding="utf-8") as f:
    channels = json.load(f)

channels = sorted(
    channels,
    key=lambda x: (x["group"], x["name"])
)

print("Generating IPTV playlist...")

with open(OUTPUT, "w", encoding="utf-8") as f:

    f.write(f'#EXTM3U x-tvg-url="{EPG_URL}"\n\n')

    current_group = ""

    for c in channels:

        if current_group != c["group"]:
            current_group = c["group"]
            f.write(f"\n# ===== {current_group} =====\n\n")

        logo = LOGOS.get(c["name"], "")

        f.write(
            f'#EXTINF:-1 '
            f'tvg-name="{c["name"]}" '
            f'tvg-logo="{logo}" '
            f'group-title="{c["group"]}",'
            f'{c["name"]}\n'
        )

        f.write(c["url"] + "\n")

print("Playlist generated.")

# README automatico
with open(README, "w", encoding="utf-8") as f:

    f.write("# IPTV Italia\n\n")
    f.write("Playlist IPTV aggiornata automaticamente.\n\n")
    f.write(f"Ultimo aggiornamento: {datetime.now()}\n\n")

    current_group = ""

    for c in channels:

        if current_group != c["group"]:
            current_group = c["group"]
            f.write(f"\n## {current_group}\n\n")

        f.write(f"- {c['name']}\n")

print("README generated.")
