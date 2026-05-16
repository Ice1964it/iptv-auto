import requests
import re
from datetime import datetime

channels = []

def add(name, url, group="Italia"):
    channels.append({
        "name": name,
        "url": url,
        "group": group
    })

# =========================
# RAI ufficiali
# =========================

rai_channels = {
    "Rai 1": "2606803",
    "Rai 2": "308718",
    "Rai 3": "308709",
    "Rai 4": "746966",
    "Rai News 24": "1"
}

for name, cid in rai_channels.items():
    url = f"https://mediapolis.rai.it/relinker/relinkerServlet.htm?cont={cid}"
    add(name, url, "RAI")

# =========================
# MEDIASET ufficiali
# =========================

mediaset = {
    "Rete 4": "r4",
    "Canale 5": "c5",
    "Italia 1": "i1",
    "20 Mediaset": "ka",
    "Focus": "fu"
}

for name, code in mediaset.items():
    url = f"https://live3-mediaset-it.akamaized.net/content/hls_h0_clr_vos/live/channel({code})/index.m3u8"
    add(name, url, "MEDIASET")

# =========================
# DISCOVERY / WARNER
# =========================

discovery = {
    "NOVE": "https://dplayit-lh.akamaihd.net/i/dmax_italy@122424/master.m3u8",
    "Real Time": "https://dplayit-lh.akamaihd.net/i/realtime_italy@128548/master.m3u8",
    "DMAX": "https://dplayit-lh.akamaihd.net/i/dmax_italy@122424/master.m3u8",
    "HGTV": "https://dplayit-lh.akamaihd.net/i/hgtv_italy@152075/master.m3u8",
    "Food Network": "https://dplayit-lh.akamaihd.net/i/foodnetwork_it@147548/master.m3u8"
}

for name, url in discovery.items():
    add(name, url, "DISCOVERY")

# =========================
# LA7
# =========================

add(
    "La7",
    "https://la7live-lh.akamaihd.net/i/La7_1@48907/master.m3u8",
    "LA7"
)

# =========================
# TV8
# =========================

add(
    "TV8",
    "https://sky-live.fl.freecaster.net/live/tv8/tv8.stream/playlist.m3u8",
    "SKY"
)

# =========================
# RSI Svizzera Italiana
# =========================

add(
    "RSI LA1",
    "https://lsaplus.swisstxt.ch/audio/video/la1_720.stream/chunklist_DVR.m3u8",
    "SVIZZERA"
)

add(
    "RSI LA2",
    "https://lsaplus.swisstxt.ch/audio/video/la2_720.stream/chunklist_DVR.m3u8",
    "SVIZZERA"
)

# =========================
# MUSICA
# =========================

music = {
    "Radio Italia TV":
        "https://radioitaliatv.akamaized.net/hls/live/2093117/RadioItaliaTV/index.m3u8",

    "RTL 102.5 TV":
        "https://rtl-radio-streaming.akamaized.net/hls/live/2043153/rtl1025/master.m3u8"
}

for name, url in music.items():
    add(name, url, "MUSICA")

# =========================
# Scrittura M3U
# =========================

filename = "italia.m3u"

with open(filename, "w", encoding="utf-8") as f:
    f.write("#EXTM3U\n")

    for ch in channels:
        f.write(
            f'#EXTINF:-1 group-title="{ch["group"]}",{ch["name"]}\n'
        )
        f.write(ch["url"] + "\n")

print(f"\nPlaylist generata: {filename}")
print(f"Canali: {len(channels)}")
print("Aggiornata:", datetime.now())