import yt_dlp

# Target a live stream or channel you want to track
CHANNEL_URL = 'YOUR_TARGET_YOUTUBE_LIVE_OR_CHANNEL_URL'

ydl_opts = {
    'format': 'bv*+ba/b',  # Ensures best video + best audio combined format
    'skip_download': True,
    'extract_flat': False, # Needs to be False to extract direct media URLs
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(CHANNEL_URL, download=False)
        
        # If it's a channel, grab entries; if direct video, wrap it in a list
        entries = info.get('entries', [info])
        
        with open('playlist.m3u', 'w', encoding='utf-8') as f:
            f.write("#EXTM3U\n")
            for entry in entries:
                if entry and entry.get('is_live'):
                    title = entry.get('title', 'Live Stream')
                    stream_url = entry.get('url')
                    if stream_url:
                        f.write(f"#EXTINF:-1,{title}\n{stream_url}\n")
                        
    print("Playlist generated successfully with audio/video formats.")
except Exception as e:
    print(f"Error generation failed: {e}")
