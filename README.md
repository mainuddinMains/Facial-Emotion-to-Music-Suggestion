#  Emotion to Song Matcher (via Groq)

A fun AI-powered tool that detects your emotion and uses **Groq AI** to suggest matching songs!

## Features
- Uses **HuggingFace FER model** (`dima806/facial_emotions_image_detection`) for emotion detection
- Uses **Groq API** (`llama3-8b-8192`) for dynamic song suggestions
- Optional genre preference input

## Tools Used
- HuggingFace Transformers
- Groq AI API
- Gradio for UI

## Requirements
See `requirements.txt`

## How to Run Locally

1. Clone repo:
   ```bash
   git clone https://github.com/yourusername/emotion-music-matcher.git
   cd emotion-music-matcher