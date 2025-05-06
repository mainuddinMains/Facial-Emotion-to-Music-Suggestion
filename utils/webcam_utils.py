# webcam_utils.py
import cv2

def capture_webcam_frame(save_path="webcam_capture.jpg"):
    """
    Captures a single frame from the webcam and saves it.
    Returns path to saved image or None if failed.
    """
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(save_path, frame)
    cap.release()
    return save_path if ret else None