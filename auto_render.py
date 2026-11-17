import urllib.request
import re
import subprocess
import time
import os

PLAYLIST_URL = "https://raw.githubusercontent.com/srhady/willow-event/refs/heads/main/live_sports.m3u"
OUTPUT_DIR = "/app/live_stream"

def fetch_and_stream():
    print("Fetching playlist...")
    try:
        req = urllib.request.Request(PLAYLIST_URL, headers={'User-Agent': 'Mozilla/5.0'})
        content = urllib.request.urlopen(req).read().decode('utf-8')
        
        key_match = re.search(r'license_key=([a-f0-9]+):([a-f0-9]+)', content)
        mpd_match = re.search(r'(https?://[^\s]+\.mpd)', content)
        
        if not key_match or not mpd_match:
            return
            
        kid, dec_key = key_match.groups()
        mpd_url = mpd_match.group(1)
        
        # Render-এর সার্ভারে 720p-তে রেন্ডার
        ffmpeg_cmd = [
            "ffmpeg", "-nostdin",
            "-reconnect", "1", "-reconnect_at_eof", "1", "-reconnect_streamed", "1", "-reconnect_delay_max", "2",
            "-cenc_decryption_key", dec_key, 
            "-i", mpd_url,
            "-vf", "scale=-2:720", 
            "-c:v", "libx264", "-preset", "superfast", "-b:v", "1500k", 
            "-c:a", "aac", "-b:a", "128k",
            "-f", "hls", "-hls_time", "4", "-hls_list_size", "30",
            "-hls_flags", "delete_segments+omit_endlist",
            "index.m3u8"
        ]
        subprocess.run(ffmpeg_cmd)
    except Exception as e:
        pass

while True:
    fetch_and_stream()
    time.sleep(10)
