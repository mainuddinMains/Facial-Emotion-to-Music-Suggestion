# emotion_detector.py
from transformers import pipeline

# Load the emotion classifier
emotion_classifier = pipeline('image-classification', model='dima806/facial_emotions_image_detection')

def detect_emotion(image_path):
    """
    Detects emotion from an image file.
    Returns dominant emotion label and confidence score.
    """
    results = emotion_classifier(image_path)
    dominant_label = results[0]['label']
    confidence = results[0]['score']
    return dominant_label, confidence

emotion_classifier = pipeline(
    'image-classification', 
    model='dima806/facial_emotions_image_detection',
    device="mps",  # For Apple Silicon
    use_fast=True  # Explicitly enable fast processor
)