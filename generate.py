import json
import requests
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

PLAYLIST_OUTPUT = "playlist.m3u"
OFFLINE_OUTPUT = "offline.m3u"
LOG_OUTPUT = "check.log"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 Chrome/122 Safari/537.36"
    )
}

# sessione stabile con retry
session = requests.Session()

retries = Retry(
    total=2,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)

session.mount("http://", HTTPAdapter(max_retries=retries))
session.mount("https://", HTTPAdapter(max_retries=retries))


def check_stream(url):
    """
    Verifica stream IPTV senza essere troppo aggressivo.
    """
    try:
        r = session.get(
            url,
            timeout=10,
            headers=HEADERS,
            allow_redirects=True,
            stream=True
        )

        # molti stream IPTV usano questi codici
        if r.status_code < 500:
            return True, r.status_code

        return False, r.status_code

    except Exception as e:
        return False, str(e)


# carica canali
with open("channels.json", "r", encoding="utf-8") as f:
    channels = json.load(f)

online = []
offline = []

print("\nChecking IPTV streams...\n")

log_lines = []

for c in channels:

    ok, info = check_stream(c["url"])

    if ok:
        print(f"OK   {c['name']} ({info})")
        online.append(c)
        log_lines.append(f"[OK] {c['name']} -> {info}")

    else:
        print(f"OFF  {c['name']} ({info})")

        # NON scartiamo il canale
        # lo mettiamo comunque nella playlist principale
        online.append(c)

        offline.append(c)
        log_lines.append(f"[OFF] {c['name']} -> {info}")

# =========================
# PLAYLIST PRINCIPALE
# =========================

with open(PLAYLIST_OUTPUT, "w", encoding="utf-8") as f:

    f.write("#EXTM3U\n")
    f.write(f"# Generated: {datetime.now().isoformat()}\n\n")

    for c in online:

        f.write(
            f'#EXTINF:-1 group-title="{c["group"]}",{c["name"]}\n'
        )

        f.write(c["url"] + "\n")

# =========================
# PLAYLIST OFFLINE
# =========================

with open(OFFLINE_OUTPUT, "w", encoding="utf-8") as f:

    f.write("#EXTM3U\n")
    f.write(f"# Offline generated: {datetime.now().isoformat()}\n\n")

    for c in offline:

        f.write(
            f'#EXTINF:-1 group-title="{c["group"]}",{c["name"]}\n'
        )

        f.write(c["url"] + "\n")

# =========================
# LOG FILE
# =========================

with open(LOG_OUTPUT, "w", encoding="utf-8") as f:
    f.write("\n".join(log_lines))

print("\n=========================")
print("Playlist generated")
print("=========================")
print("Total channels :", len(channels))
print("Main playlist  :", len(online))
print("Offline list   :", len(offline))
print("Date           :", datetime.now())
