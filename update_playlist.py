import yt_dlp

# Your list of channels
CHANNELS = [
    "https://www.youtube.com/france24english/live",
    "https://www.youtube.com/africanews/live",
    "https://www.youtube.com/euronews/live",
    "https://www.youtube.com/@SkyNews/live",
    "https://www.youtube.com/@aljazeeraenglish/live",
    "https://www.youtube.com/@NASA/live",
    "https://www.youtube.com/@SpaceX/live",
    "https://www.youtube.com/@NASASpaceflight/live",
    "https://www.youtube.com/@earthcam/live",
    "https://www.youtube.com/@WorldCamLIVE/live",
    "https://www.youtube.com/@explore/live",
    "https://www.youtube.com/@bbcearth/live",
    "https://www.youtube.com/@NatGeo/live",
    "https://www.youtube.com/@ESA/live",
    "https://www.youtube.com/@JAXA-official/live",
    "https://www.youtube.com/@Sen/live",
    "https://www.youtube.com/@SputnikNews/live",
    "https://www.youtube.com/@abcnewsaustralia/live",
    "https://www.youtube.com/tvcnewsnigeria/live",
    "https://www.youtube.com/channelstelevision/live",
    "https://www.youtube.com/channel/UC83jt4dlz1Gjl58fzQrrKZg/live",
    "https://www.youtube.com/channel/UCoMdktPbSTixAyNGwb-UYkQ/live",
    "https://www.youtube.com/channel/UCZFMm1mMw0F81Z37aaEzTUA/live",
    "https://www.youtube.com/channel/UCGDQNvybfDDeGTf4GtigXaw/live",
    "https://www.youtube.com/channel/UC_gUM8rL-Lrg6O3adPW9K1g/live",
    "https://www.youtube.com/channel/UChd1DEecCRlxaa0-hvPACCw/live",
    "https://www.youtube.com/channel/UC0vn8ISa4LKMunLbzaXLnOQ/live"
]

ydl_opts = {
    # 'best' or format 22/18 ensures we grab a stream containing both audio and video
    'format': 'best/b',
    'skip_download': True,
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
