import json
import subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

channels_dir = BASE / "channels"
output_dir = BASE / "output"

playlist = "#EXTM3U\n\n"

def get_stream(url):
    try:
        stream = subprocess.check_output(
            ["yt-dlp", "-g", url],
            text=True
        ).strip()

        return stream

    except Exception as e:
        print(f"Errore: {url}")
        print(e)
        return None


for file in channels_dir.glob("*.json"):

    with open(file, "r", encoding="utf-8") as f:
        channels = json.load(f)

    for ch in channels:

        print(f"Estrazione: {ch['name']}")

        stream = get_stream(ch["page"])

        if stream:

            playlist += (
                f'#EXTINF:-1 group-title="{ch["group"]}",'
                f'{ch["name"]}\n'
                f'{stream}\n\n'
            )

output_dir.mkdir(exist_ok=True)

with open(output_dir / "playlist.m3u", "w", encoding="utf-8") as f:
    f.write(playlist)

print("Playlist generata!")
