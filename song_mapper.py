# # song_mapper.py
# from groq import Groq
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# # Initialize Groq client
# client = Groq(api_key=GROQ_API_KEY)

# def get_groq_suggestion(emotion, genre=None):
#     try:
#         prompt = f"Suggest a song that matches the emotion '{emotion}'."
#         if genre:
#             prompt += f" Preferably in the '{genre}' genre."

#         chat_completion = client.chat.completions.create(
#             messages=[
#                 {"role": "system", "content": "You are a helpful assistant."},
#                 {"role": "user", "content": prompt}
#             ],
#             model="llama3-8b-8192",
#             max_tokens=64,
#             temperature=0.7,
#             top_p=1.0
#         )

#         return chat_completion.choices[0].message.content.strip()



#     except Exception as e:
#         return f"Could not generate song suggestion. Error: {str(e)}"


# song_mapper.py
from groq import Groq
from dotenv import load_dotenv
import os
# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

FALLBACK_SONGS = {
    "sad":      ["Someone Like You by Adele", "The Night We Met by Lord Huron", "Skinny Love by Bon Iver", "Fix You by Coldplay"],
    "happy":    ["Happy by Pharrell Williams", "Can't Stop the Feeling by Justin Timberlake", "Uptown Funk by Mark Ronson", "Good as Hell by Lizzo"],
    "angry":    ["Break Stuff by Limp Bizkit", "Given Up by Linkin Park", "Killing in the Name by Rage Against the Machine", "Headstrong by Trapt"],
    "neutral":  ["Weightless by Marconi Union", "Experience by Ludovico Einaudi", "Holocene by Bon Iver", "Breathe by Telepopmusik"],
    "fear":     ["Disturbia by Rihanna", "Thriller by Michael Jackson", "Monster by Imagine Dragons", "Run Boy Run by Woodkid"],
    "surprise": ["Livin on a Prayer by Bon Jovi", "Don't Stop Me Now by Queen", "Bohemian Rhapsody by Queen", "Shake It Off by Taylor Swift"],
    "disgust":  ["Creep by Radiohead", "Loser by Beck", "Basket Case by Green Day", "Boulevard of Broken Dreams by Green Day"],
}

def get_groq_suggestion(emotion: str, genre_preference: str = None) -> str:
    """Returns a song suggestion based on emotion and optional genre."""
    import random

    try:
        prompt = (
            f"Suggest a real song that matches the emotion '{emotion}'. "
            f"Reply with ONLY the song title and artist in this format: \"Song Title\" by Artist Name. "
            f"No explanation, no extra text."
        )
        if genre_preference:
            prompt = (
                f"Suggest a real {genre_preference} song that matches the emotion '{emotion}'. "
                f"Reply with ONLY the song title and artist in this format: \"Song Title\" by Artist Name. "
                f"No explanation, no extra text."
            )

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a music recommendation assistant. You only respond with a song title and artist in the format: \"Song Title\" by Artist Name."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192",
            max_tokens=64,
            temperature=0.7,
        )

        return chat_completion.choices[0].message.content.strip()

    except Exception:
        songs = FALLBACK_SONGS.get(emotion.lower(), ["Bohemian Rhapsody by Queen"])
        return random.choice(songs)

