# app.py
import gradio as gr
from emotion_detector import detect_emotion
from utils.webcam_utils import capture_webcam_frame
from song_mapper import get_groq_suggestion
import cv2

def process_input(use_webcam, genre_preference=None):
    if use_webcam:
        frame = capture_webcam_frame()
        if frame is None:
            return None, "Error: Could not capture image from webcam."
    else:
        return None, "Upload support coming soon! For now, please use webcam."

    # Save temp file for emotion detection
    img_path = "webcam_capture.jpg"
    cv2.imwrite(img_path, frame)

    emotion, confidence = detect_emotion(img_path)
    song_suggestion = get_groq_suggestion(emotion, genre_preference)

    output = f"📸 Emotion Detected: **{emotion}** ({confidence:.2f})\n\n"
    output += f"🎧 Song Suggestion:\n{song_suggestion}"

    # Convert BGR to RGB for Gradio display
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    return frame_rgb, output

# Define inputs
inputs = [
    gr.Checkbox(label="Use Webcam", value=True),
    gr.Textbox(label="Preferred Genre (e.g., pop, rock)", placeholder="Optional")
]

# Define outputs
image_output = gr.Image(label="Captured Image", type="numpy")
text_output = gr.Textbox(label="Results", lines=6)

demo = gr.Interface(
    fn=process_input,
    inputs=inputs,
    outputs=[image_output, text_output],
    title="🎭 Emotion to Song Matcher (via Groq)",
    description="Detects your emotion and lets Groq AI suggest songs!",
    allow_flagging="never"
)

if __name__ == "__main__":
    demo.launch()