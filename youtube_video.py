# youtube_video.py
from googleapiclient.discovery import build
from urllib.parse import quote
import os
import time
from pytube import Search


def get_youtube_video_url(song_query: str, max_retries=2) -> str:
    """Returns YouTube watch URL for the song with retry logic"""
    youtube = build('youtube', 'v3', developerKey=os.getenv("YT_API_KEY"))
    
    for attempt in range(max_retries):
        try:
            request = youtube.search().list(
                q=f"{song_query} official music video",
                part="id",
                maxResults=1,
                type="video",
                videoDuration="medium",
                safeSearch="none"
            )
            response = request.execute()
            
            if response.get('items'):
                return f"https://youtube.com/watch?v={response['items'][0]['id']['videoId']}"
                
        except Exception as e:
            print(f"YouTube search attempt {attempt+1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(2)  # Wait before retrying
                
    return None

def get_youtube_video_url_pytube(song_query: str) -> str:
    """Fallback using pytube when API fails"""
    try:
        s = Search(f"{song_query} official music video")
        return s.results[0].watch_url if s.results else None
    except Exception as e:
        print(f"Pytube fallback failed: {str(e)}")
        return None