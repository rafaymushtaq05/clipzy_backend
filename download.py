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

# yt-dlp options
ydl_opts = {
    'outtmpl': output_path,
    'format': 'bestvideo+bestaudio/best',
    'merge_output_format': 'mp4',
    'quiet': True,
    'no_warnings': True,
    'progress_hooks': [progress_hook],
}

# Prefer platform.json → platform.txt → instagram fallback
base_dir = os.path.dirname(__file__)
json_path = os.path.join(base_dir, 'cookies', f"{platform}.json")
txt_path = os.path.join(base_dir, 'cookies', f"{platform}.txt")
insta_fallback = os.path.join(base_dir, 'cookies', 'instagram.json')

if os.path.exists(json_path):
    ydl_opts['cookiefile'] = json_path
    print(f"[{download_id}] ✅ Using session: {json_path}", flush=True)
elif os.path.exists(txt_path):
    ydl_opts['cookiefile'] = txt_path
    print(f"[{download_id}] ✅ Using cookie: {txt_path}", flush=True)
elif os.path.exists(insta_fallback):
    ydl_opts['cookiefile'] = insta_fallback
    print(f"[{download_id}] ⚠ Using fallback: {insta_fallback}", flush=True)
else:
    print(f"[{download_id}] ❌ No valid cookie/session file found!", flush=True)

# Start download
try:
    print(f"[{download_id}] Starting download: {url}", flush=True)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print(f"[{download_id}] ✅ Download complete!", flush=True)
except Exception as e:
    print(f"[{download_id}] ❌ ERROR: {e}", flush=True)
    sys.exit(1)
