from ytmusicapi import YTMusic
from yt_dlp import YoutubeDL
import ffmpeg
import subprocess

ytmusic = YTMusic("oauth.json")

# Fetch library songs
library_results = ytmusic.get_library_songs(limit=None)


for result in library_results:
    video_id = result['videoId']
    title = result['title']
    
    # Download the video using YoutubeDL
    options = {
        'extract_flat': 'discard_in_playlist',
        'final_ext': 'm4a',
        'format': 'bestaudio/best',
        'fragment_retries': 10,
        'ignoreerrors': 'only_download',
        'outtmpl': {
            'default': '%(title)s',
            'pl_thumbnail': ''
        },
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'nopostoverwrites': False,
                'preferredcodec': 'm4a',
                'preferredquality': '5'
            },
            {
                'add_chapters': True,
                'add_infojson': 'if_exists',
                'add_metadata': True,
                'key': 'FFmpegMetadata'
            },
            {
                'already_have_thumbnail': False,
                'key': 'EmbedThumbnail'
            },
            {
                'key': 'FFmpegConcat',
                'only_multi_video': True,
                'when': 'playlist'
            }
        ],
        'retries': 10,
        'writethumbnail': True
    }
    
    YoutubeDL(options).download([video_id])
