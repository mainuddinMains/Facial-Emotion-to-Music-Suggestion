# app.py (updated with camera stabilization)
import os
import cv2
import time  # Added for delay
import re
import warnings
from urllib.parse import quote
os.environ['GRADIO_ANALYTICS_ENABLED'] = 'False'
from config import ENABLE_YOUTUBE, SUPPRESS_WARNINGS
from emotion_detector import detect_emotion
from song_mapper import get_groq_suggestion
from spotify_utils import search_song_spotify
from youtube_video import get_youtube_video_url
import gradio as gr

if SUPPRESS_WARNINGS:
    warnings.filterwarnings("ignore")
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def get_stable_webcam_frame(attempt=0):
    """Captures stable frame with automatic recovery from dark images"""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return None
    
    # Camera configuration
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)
    
    # Warm-up delay (increases with each failed attempt)
    time.sleep(0.5 + (attempt * 0.5))
    
    # Capture multiple frames to allow auto-adjustment
    for _ in range(5):
        ret, frame = cap.read()
        if not ret:
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Validate frame brightness
    if frame is not None and frame.size > 0:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if cv2.mean(gray)[0] < 30:  # Too dark threshold
            if attempt < 3:  # Max 3 retries
                return get_stable_webcam_frame(attempt + 1)
            return None
    
    return frame if ret else None

def process_input(use_webcam: bool, genre_preference: str = None):
    # 1. Capture and verify image
    if use_webcam:
        frame = get_stable_webcam_frame()
        if frame is None or frame.size == 0:
            return None, "Error: Camera needs a moment to adjust. Please try again in a few seconds.", None, None
        
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_path = "webcam_capture.jpg"
        cv2.imwrite(img_path, frame_rgb)
    else:
        return None, "Please use webcam", None, None

    # 2. Detect emotion
    emotion, confidence = detect_emotion(img_path)
    
    # 3. Get song suggestion
    song_suggestion = get_groq_suggestion(emotion, genre_preference)
    
    # 4. Search Spotify
    track_info = search_song_spotify(
        parse_song_query(song_suggestion) or song_suggestion[:100]
    ) or {}
    
    # 5. Get YouTube video URL if enabled
    video_url = None
    if ENABLE_YOUTUBE and track_info.get('title'):
        video_url = get_youtube_video_url(f"{track_info['title']} {track_info['artist']}")
    
    # 6. Prepare output with all components
    output_text = format_output(emotion, confidence, song_suggestion, track_info, video_url)
    album_art = track_info.get('image_url')
    
    return frame_rgb, output_text, video_url, album_art

def parse_song_query(text: str) -> str:
    patterns = [
        r'"(.*?)"\s+by\s+([^\n.]+)',
        r'([^\n"“”]+)\s+-\s+([^\n.]+)',
        r'([^\n"“”]+)\s+by\s+([^\n.]+)'
    ]
    for pattern in patterns:
        if match := re.search(pattern, text):
            return f"{match.group(1)} {match.group(2)}"
    return None

def format_output(emotion, confidence, suggestion, track_info, video_url=None):
    msg = f"""
    <div style='margin-bottom: 20px;'>
        <h2 style='color: #4a6fa5;'>🎭 Detected Emotion: {emotion.title()} ({confidence:.0%} confidence)</h2>
        <h3 style='color: #5e6ad2;'>🎵 AI Recommendation:</h3>
    """
    
    if track_info:
        msg += f"""
        <div style='background: #f5f5f5; padding: 15px; border-radius: 10px; margin-top: 20px;'>
            <h3 style='color: #4a6fa5;'>💿 {track_info.get('title', 'Unknown')}</h3>
            <p style='font-size: 16px; color: #000000;'>by {track_info.get('artist', 'Unknown')}</p>
            <div style='margin-top: 15px;'>
                {f"<a href='{video_url}' target='_blank' style='background: #ff0000; color: white; padding: 8px 16px; border-radius: 4px; text-decoration: none; margin-right: 10px;'>▶ Watch on YouTube</a>" if video_url else ""}
                {f"<a href='{track_info['spotify_url']}' target='_blank' style='background: #1DB954; color: white; padding: 8px 16px; border-radius: 4px; text-decoration: none;'>🎧 Listen on Spotify</a>" if track_info.get('spotify_url') else ""}
            </div>
        </div>
        """
    return msg

with gr.Blocks(theme=gr.themes.Soft(), title="Emotion Music Matcher") as demo:
    gr.Markdown("""
    # 🎧 Emotion-Based Music Recommender
    *Detect your mood through your webcam and discover matching songs!*
    """)
    
    with gr.Row():
        with gr.Column(scale=1):
            webcam_toggle = gr.Checkbox(label="Use Webcam", value=True)
            genre_input = gr.Textbox(label="Preferred Genre (optional)")
            submit_btn = gr.Button("Find My Song!", variant="primary")
            
        with gr.Column(scale=2):
            webcam_image = gr.Image(
                label="Your Expression", 
                height=300,
                interactive=False
            )
            output_html = gr.HTML()
            
            # Hidden components for media
            video_player = gr.Video(visible=False)
            album_art = gr.Image(label="Album Cover", visible=True, height=300)

    
    submit_btn.click(
        fn=process_input,
        inputs=[webcam_toggle, genre_input],
        outputs=[webcam_image, output_html, video_player, album_art]
    )

if __name__ == "__main__":
    demo.launch()