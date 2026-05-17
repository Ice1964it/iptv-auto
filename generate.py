import json
from datetime import datetime

OUTPUT = "playlist.m3u"

# EPG pubblica
EPG_URL = "https://epgshare01.online/epgshare01/epg_ripper_IT1.xml.gz"

# Loghi canali
LOGOS = {
    "Rai News 24": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/RaiNews24.svg/512px-RaiNews24.svg.png",
    "Rai 3": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Rai_3_-_Logo_2016.svg/512px-Rai_3_-_Logo_2016.svg.png",
    "Canale 5": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Canale_5_-_2018.svg/512px-Canale_5_-_2018.svg.png",
    "Italia 1": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Italia1.svg/512px-Italia1.svg.png",
    "Rete 4": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Rete_4_-_2018.svg/512px-Rete_4_-_2018.svg.png",
    "TV8": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/TV8_logo.svg/512px-TV8_logo.svg.png",
    "La7": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/LA7_-_Logo_2011.svg/512px-LA7_-_Logo_2011.svg.png",
    "Radio Italia TV": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Radio_Italia_TV_logo.svg/512px-Radio_Italia_TV_logo.svg.png",
    "RTL 102.5 TV": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/RTL_102.5_logo.svg/512px-RTL_102.5_logo.svg.png"
}

with open("channels.json", "r", encoding="utf-8") as f:
    channels = json.load(f)

# Ordina gruppi e nomi
channels = sorted(
    channels,
    key=lambda x: (x["group"].lower(), x["name"].lower())
)

print("Generating IPTV playlist...")

with open(OUTPUT, "w", encoding="utf-8") as f:

    # Header M3U con EPG
    f.write(f'#EXTM3U x-tvg-url="{EPG_URL}"\n\n')

    f.write(f"# Generated: {datetime.now()}\n\n")

    current_group = ""

    for c in channels:

        # separatore gruppi
        if c["group"] != current_group:
            current_group = c["group"]
            f.write(f"\n# ===== {current_group} =====\n\n")

        logo = LOGOS.get(c["name"], "")

        print(f"ADD {c['name']}")

        f.write(
            f'#EXTINF:-1 '
            f'tvg-name="{c["name"]}" '
            f'tvg-logo="{logo}" '
            f'group-title="{c["group"]}",'
            f'{c["name"]}\n'
        )

        f.write(c["url"] + "\n")

print("Playlist generated.")
print("Channels:", len(channels))
