# song_mapper.py
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

def get_groq_suggestion(emotion, genre=None):
    try:
        prompt = f"Suggest a song that matches the emotion '{emotion}'."
        if genre:
            prompt += f" Preferably in the '{genre}' genre."

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            model="llama3-8b-8192",
            max_tokens=64,
            temperature=0.7,
            top_p=1.0
        )

        return chat_completion.choices[0].message.content.strip()

    except Exception as e:
        return f"Could not generate song suggestion. Error: {str(e)}"