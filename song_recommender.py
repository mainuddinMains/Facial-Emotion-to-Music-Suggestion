# from typing import Optional, Dict
# from spotify_utils import search_song_spotify

# def search_song_spotify_by_emotion(emotion: str) -> Optional[Dict]:
#     """Search Spotify for a song based on emotion."""
#     emotion_to_query = {
#         "happy": "Happy upbeat song",
#         "sad": "Sad emotional song",
#         "angry": "Angry rock song",
#         "neutral": "Relaxing instrumental",
#         "exciting": "Exciting party song",
#         "fear": "Dark suspenseful music",
#     }
#     query = emotion_to_query.get(emotion.lower(), "Mood music")
#     return search_song_spotify(query)

from typing import Optional, Dict
import random
from spotify_utils import search_song_spotify

def get_song_recommendation(emotion: str) -> Optional[Dict]:
    """Search Spotify for a song based on emotion."""
    emotion_to_queries = {
        "happy": ["Happy upbeat song", "Feel-good music", "Cheerful pop song"],
        "sad": ["Sad emotional song", "Heartbreaking ballad", "Melancholic tune"],
        "angry": ["Angry rock song", "Intense metal track", "Aggressive rap song"],
        "neutral": ["Relaxing instrumental", "Chill background music", "Ambient sounds"],
        "exciting": ["Exciting party song", "High-energy dance track", "Upbeat electronic music"],
        "fear": ["Dark suspenseful music", "Eerie soundtrack", "Horror movie score"],
    }
    queries = emotion_to_queries.get(emotion.lower(), ["Mood music"])
    query = random.choice(queries)  # Randomly select a query
    print(f"Selected query for emotion '{emotion}': {query}")  # Debug print
    result = search_song_spotify(query)
    print(f"Spotify result for query '{query}': {result}")  # Debug print
    return result