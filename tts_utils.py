# tts_utils.py
from gtts import gTTS
import os

def create_tts_fallback(song_name, artist):
    text = f"Recommended: {song_name} by {artist}. No preview available."
    tts = gTTS(text=text, lang='en')
    tts.save("tts_fallback.mp3")
    return "tts_fallback.mp3"