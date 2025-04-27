"""
Configuration settings and constants for the gesture media controller.
"""
import os

# Constants
GESTURE_THRESHOLD = 0.05
VOLUME_SENSITIVITY = 0.1
GESTURE_COOLDOWN = 0.7  # Slightly faster cooldown for regular gestures

# Path to the MediaPipe gesture recognizer model
MODEL_PATH =  "models/gesture_recognizer.task"

# Default control mode settings
DEFAULT_CONTROL_MODES = {
    "voice": False,
    "gesture": True,
    "face": True
}
