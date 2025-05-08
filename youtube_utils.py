from pytube import YouTube, Search
from typing import Optional
import re
import os
import time
from urllib.parse import quote

def sanitize_query(query: str) -> str:
    """Advanced query cleaning"""
    query = re.sub(r'[^\w\s-]', '', query)
    query = re.sub(r'\s+', ' ', query).strip()
    return quote(query[:50])  # URL-encode the query

def get_youtube_audio(song_query: str, max_attempts=2) -> Optional[str]:
    for attempt in range(max_attempts):
        try:
            clean_query = sanitize_query(f"{song_query} official audio")
            s = Search(clean_query)
            
            # Wait between attempts
            if attempt > 0:
                time.sleep(1)
                
            for video in s.results[:3]:  # Limit to top 3 results
                try:
                    if video.length and video.length <= 300:
                        stream = video.streams.filter(only_audio=True).first()
                        if stream:
                            temp_file = f"temp_{video.video_id}.mp3"
                            stream.download(filename=temp_file)
                            return temp_file
                except Exception:
                    continue
                    
        except Exception as e:
            if attempt == max_attempts - 1:  # Last attempt
                print(f"YouTube fallback failed after {max_attempts} attempts")
            continue
            
    return None