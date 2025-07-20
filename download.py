import sys
import yt_dlp
import os

# Args: url, output_path, download_id, platform
url = sys.argv[1]
output_path = sys.argv[2]
download_id = sys.argv[3]
platform = sys.argv[4].lower()

def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '').strip()
        if percent:
            print(f"[{download_id}] {percent} complete", flush=True)
    elif d['status'] == 'finished':
        print(f"[{download_id}] Merging audio and video. Please wait...", flush=True)

# Base options
ydl_opts = {
    'outtmpl': output_path,
    'format': 'bestvideo+bestaudio/best',
    'merge_output_format': 'mp4',
    'quiet': True,
    'no_warnings': True,
    'progress_hooks': [progress_hook],
}

# Add cookie file if it exists
cookie_file = os.path.join(os.path.dirname(__file__), 'cookies', f"{platform}.txt")
if os.path.exists(cookie_file):
    ydl_opts['cookiefile'] = cookie_file  # ✅ correct key
    print(f"[{download_id}] ✅ Using cookie file: {cookie_file}", flush=True)
else:
    print(f"[{download_id}] ⚠ No cookie file found for {platform}", flush=True)

# Start download
try:
    print(f"[{download_id}] Starting download: {url}", flush=True)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print(f"[{download_id}] ✅ Download complete!", flush=True)
except Exception as e:
    print(f"[{download_id}] ❌ ERROR: {e}", flush=True)
    sys.exit(1)
