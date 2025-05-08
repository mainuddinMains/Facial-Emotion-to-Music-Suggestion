# Emotion-Based Music Recommender 🎭→🎧

![Project Demo](assets/demo.gif) 

## Project Description
A real-time emotion detection system that suggests music based on your current mood. The application:
1. Captures your facial expression via webcam
2. Detects your emotion using AI
3. Recommends a matching song using Groq's LLM
4. Provides Spotify links and album artwork
5. Optionally shows YouTube music videos

## Key Features
- Real-time facial emotion detection
- AI-powered song recommendations
- Spotify integration with album art
- YouTube video links
- Clean, responsive Gradio interface

## Technologies Used

### Core Components
| Component | Technology |
|-----------|------------|
| Emotion Detection | `dima806/facial_emotions_image_detection` (Hugging Face) |
| LLM Suggestions | Groq API (Llama3-8b) |
| Music Metadata | Spotify API |
| Video Links | YouTube Data API |
| Interface | Gradio |

### Python Libraries
transformers
torch
opencv-python
gradio
groq
spotipy
pytube
google-api-python-client
python-dotenv


## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- Webcam
- API keys for:
  - Groq
  - Spotify
  - YouTube (optional)

### 2. Installation
```bash
# Clone the repository
git clone https://github.com/your-username/emotion-music-recommender.git
cd emotion-music-recommender

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration
Create a .env file with your API keys:
```bash
#.env
GROQ_API_KEY=your_groq_key_here
SPOTIPY_CLIENT_ID=your_spotify_client_id
SPOTIPY_CLIENT_SECRET=your_spotify_secret
YT_API_KEY=your_youtube_key  # Optional
```

### 4. Running the Application
```bash
python app.py
```
The interface will launch at http://localhost:7860