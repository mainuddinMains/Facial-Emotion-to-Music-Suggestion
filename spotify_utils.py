# spotify_utils.py
import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials
from typing import Optional, Dict

# Load environment variables
load_dotenv()

# Setup Spotify client
def get_spotify_client():
    try:
        return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET")
        ))
    except Exception as e:
        print(f"Error initializing Spotify client: {str(e)}")
        return None

sp = get_spotify_client()

def search_song_spotify(query: str) -> Optional[Dict]:
    """
    Improved Spotify search with better error handling and query parsing
    Returns: {
        "title": str,
        "artist": str,
        "preview_url": Optional[str],
        "image_url": Optional[str],
        "spotify_url": Optional[str]
    } or None
    """
    if not sp or not query:
        return None

    try:
        # Clean query - remove quotes and 'by' for better search
        clean_query = query.replace('"', '').replace("'", "").replace("by", "")
        results = sp.search(q=clean_query, limit=1, type='track', market="US")
        
        if not results['tracks']['items']:
            return None

        track = results['tracks']['items'][0]
        return {
            "title": track['name'],
            "artist": track['artists'][0]['name'],
            "preview_url": track.get('preview_url'),
            "image_url": track['album']['images'][0]['url'] if track['album']['images'] else None,
            "spotify_url": track['external_urls']['spotify']
        }
    except Exception as e:
        print(f"Spotify search error for query '{query}': {str(e)}")
        return None

def find_similar_with_preview(artist_id, original_title):
    try:
        results = sp.artist_top_tracks(artist_id)
        for track in results['tracks']:
            if track['preview_url'] and track['name'] != original_title:
                return {
                    "title": track['name'],
                    "artist": track['artists'][0]['name'],
                    "preview_url": track['preview_url'],
                    "image_url": track['album']['images'][0]['url'],
                    "fallback_reason": f"No preview for '{original_title}'"
                }
    except Exception as e:
        print(f"Similar tracks search failed: {str(e)}")
    return None