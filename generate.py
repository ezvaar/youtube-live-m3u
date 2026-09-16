#!/usr/bin/env python3
"""Generate a YouTube Live M3U playlist with real m3u8 streams."""

import yt_dlp
from datetime import datetime, timezone

CHANNELS = [
    ("France 24 English", "https://www.youtube.com/france24english/live"),
    ("Africanews", "https://www.youtube.com/africanews/live"),
    ("Euronews", "https://www.youtube.com/euronews/live"),
    ("Sky News", "https://www.youtube.com/@SkyNews/live"),
    ("Al Jazeera English", "https://www.youtube.com/@aljazeeraenglish/live"),
    ("NASA Live", "https://www.youtube.com/@NASA/live"),
    ("SpaceX", "https://www.youtube.com/@SpaceX/live"),
    ("NASASpaceflight", "https://www.youtube.com/@NASASpaceflight/live"),
    ("EarthCam", "https://www.youtube.com/@earthcam/live"),
    ("WorldCam LIVE", "https://www.youtube.com/@WorldCamLIVE/live"),
    ("Explore.org", "https://www.youtube.com/@explore/live"),
    ("BBC Earth", "https://www.youtube.com/@bbcearth/live"),
    ("National Geographic", "https://www.youtube.com/@NatGeo/live"),
    ("ESA", "https://www.youtube.com/@ESA/live"),
    ("JAXA", "https://www.youtube.com/@JAXA-official/live"),
    ("Sen (Earth from ISS)", "https://www.youtube.com/@Sen/live"),
    ("Sputnik", "https://www.youtube.com/@SputnikNews/live"),
    ("ABC News Australia", "https://www.youtube.com/@abcnewsaustralia/live"),
    ("TVC News Nigeria", "https://www.youtube.com/tvcnewsnigeria/live"),
    ("Channels TV Nigeria", "https://www.youtube.com/channelstelevision/live"),
    ("Channel News Asia", "https://www.youtube.com/channel/UC83jt4dlz1Gjl58fzQrrKZg/live"),
    ("Sky News (alt)", "https://www.youtube.com/channel/UCoMdktPbSTixAyNGwb-UYkQ/live"),
    ("NDTV 24x7", "https://www.youtube.com/channel/UCZFMm1mMw0F81Z37aaEzTUA/live"),
    ("DD India", "https://www.youtube.com/channel/UCGDQNvybfDDeGTf4GtigXaw/live"),
    ("WION", "https://www.youtube.com/channel/UC_gUM8rL-Lrg6O3adPW9K1g/live"),
    ("Joy News", "https://www.youtube.com/channel/UChd1DEecCRlxaa0-hvPACCw/live"),
    ("GB News", "https://www.youtube.com/channel/UC0vn8ISa4LKMunLbzaXLnOQ/live"),
]

ydl_opts = {
    "format": "best[protocol^=m3u8]/best",
    "skip_download": True,
    "quiet": True,
    "no_warnings": True,
    "ignoreerrors": True,
}

def get_best_m3u8(info):
    if not info:
        return None
    formats = info.get("formats") or []
    hls = [f for f in formats if f.get("protocol") in ("m3u8", "m3u8_native") and f.get("url")]
    if hls:
        hls.sort(key=lambda x: x.get("height") or 0, reverse=True)
        return hls[0]["url"]
    return info.get("url")

def generate_playlist():
    print("Generating YouTube Live playlist...")
    valid = 0
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    with open("youtube-live.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write(f"# Updated: {now}\n")
        f.write("# Auto-generated with yt-dlp – links expire after a few hours\n\n")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for name, url in CHANNELS:
                print(f"Checking: {name}")
                try:
                    info = ydl.extract_info(url, download=False)
                    if not info:    'skip_download': True,
    'extract_flat': False,
    'ignoreerrors': True,  # Prevents script from crashing if a channel is offline or errors out
}

def generate_playlist():
    print("Starting M3U playlist generation...")
    valid_streams = 0

    with open('playlist.m3u', 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            for url in CHANNELS:
                try:
                    print(f"Checking: {url}")
                    info = ydl.extract_info(url, download=False)
                    
                    if not info:
                        continue
                        
                    # Check if it's currently live
                    if info.get('is_live') or info.get('live_status') == 'is_live':
                        title = info.get('title', 'Live Stream')
                        stream_url = info.get('url')
                        
                        if stream_url:
                            f.write(f"#EXTINF:-1,{title}\n{stream_url}\n")
                            valid_streams += 1
                            print(f" [OK] Added live stream: {title}")
                    else:
                        print(f" [OFFLINE] Channel is not live right now.")
                except Exception as e:
                    print(f" [ERROR] Could not fetch {url}: {e}")

    print(f"Playlist generation complete. Total active streams added: {valid_streams}")

if __name__ == '__main__':
    generate_playlist()
