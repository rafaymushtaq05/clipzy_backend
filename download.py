import sys
import yt_dlp

url = sys.argv[1]
output_path = sys.argv[2]
download_id = sys.argv[3]

def progress_hook(d):
    if d['status'] == 'downloading':
        percent = d.get('_percent_str', '').strip()
        if percent:
            print(f"[{download_id}] {percent} complete", flush=True)
    elif d['status'] == 'finished':
        print(f"[{download_id}] Merging audio and video. Please wait...", flush=True)

ydl_opts = {
    'outtmpl': output_path,
    'format': 'bestvideo+bestaudio/best',
    'merge_output_format': 'mp4',
    'progress_hooks': [progress_hook],
    'quiet': True,
    'no_warnings': True
}

try:
    print(f"[{download_id}] Starting download: {url}", flush=True)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print(f"[{download_id}] Download complete!", flush=True)
except Exception as e:
    print(f"[{download_id}] ERROR: {e}", flush=True)
    sys.exit(1)
