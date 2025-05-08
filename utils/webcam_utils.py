# webcam_utils.py
import cv2

def capture_webcam_frame():
    """
    Captures a single frame from the webcam and returns it as a BGR image array.
    Returns None if capture fails.
    """
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    return frame if ret else None