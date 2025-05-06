# app.py
import gradio as gr
from emotion_detector import detect_emotion
from utils.webcam_utils import capture_webcam_frame
from song_mapper import get_groq_suggestion

def process_input(use_webcam, genre_preference=None):
    if use_webcam:
        img_path = capture_webcam_frame()
        if not img_path:
            return "Error: Could not capture image from webcam."
    else:
        return "Upload support coming soon! For now, please use webcam."

    emotion, confidence = detect_emotion(img_path)
    song_suggestion = get_groq_suggestion(emotion, genre_preference)

    output = f"📸 Emotion Detected: **{emotion}** ({confidence:.2f})\n\n"
    output += f"🎧 Song Suggestion:\n{song_suggestion}"

    return output

# Gradio Interface
inputs = [
    gr.Checkbox(label="Use Webcam", value=True),
    gr.Textbox(label="Preferred Genre (e.g., pop, rock)", placeholder="Optional")
]
output = gr.Textbox(label="Results")

title = "🎭 Emotion to Song Matcher (via Groq)"
description = "Detects your emotion and lets Groq AI suggest songs!"

demo = gr.Interface(fn=process_input, inputs=inputs, outputs=output, title=title, description=description)

if __name__ == "__main__":
    demo.launch()