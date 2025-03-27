"""
Gesture detection and control for media playback using MediaPipe's Gesture Recognizer.
"""
import time
import os
import pyautogui
import mediapipe as mp
import cv2
import numpy as np
import urllib.request
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from ..config import GESTURE_COOLDOWN, VOLUME_SENSITIVITY, MODEL_PATH


class GestureController:
    """
    Controls media player based on hand gestures using MediaPipe's pre-trained gesture recognizer.
    """
    def __init__(self, audio_controller):
        """
        Initialize the gesture controller with MediaPipe's gesture recognizer.
        
        Args:
            audio_controller: Instance of AudioController for volume control
        """
        self.audio_controller = audio_controller
        self.last_gesture_time = 0
        self.previous_gesture = None
        self.gesture_start_time = 0
        self.last_toggle_time = 0
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Download and set up the gesture recognizer model
        self._setup_gesture_recognizer()
        
    def _setup_gesture_recognizer(self):
        """Download and set up the MediaPipe gesture recognizer."""
        model_path = MODEL_PATH
        
        # Create the model directory if it doesn't exist
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        
        # Download the model if it doesn't exist
        if not os.path.exists(model_path):
            print("Downloading MediaPipe gesture recognizer model...")
            url = "https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/1/gesture_recognizer.task"
            urllib.request.urlretrieve(url, model_path)
            print("Model downloaded successfully.")
        
        # Initialize the gesture recognizer
        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.GestureRecognizerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            num_hands=1,
            min_hand_detection_confidence=0.5,
            min_hand_presence_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.recognizer = vision.GestureRecognizer.create_from_options(options)
        
    def process_frame(self, frame):
        """
        Process a video frame to detect hand gestures using MediaPipe's gesture recognizer.
        
        Args:
            frame: OpenCV image frame
        
        Returns:
            processed_frame: Frame with hand landmarks and gesture info
            detected_gesture: Name of detected gesture or None
        """
        # Convert OpenCV BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Create MediaPipe Image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        try:
            # Recognize gestures
            recognition_result = self.recognizer.recognize(mp_image)
            
            # Process results
            if not recognition_result.gestures or not recognition_result.hand_landmarks:
                # Display "No Hand Detected" when no hand is found
                cv2.putText(frame, "No Hand Detected", (10, 70), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                self.previous_gesture = None
                return frame, None
                
            # Get the top gesture and hand information
            top_gesture = recognition_result.gestures[0][0]
            gesture_name = top_gesture.category_name
            gesture_score = top_gesture.score
            hand_landmarks = recognition_result.hand_landmarks[0]
            
            # Draw hand landmarks on the frame
            self._draw_landmarks(frame, hand_landmarks)
            
            # Display gesture information on frame
            confidence = int(gesture_score * 100)
            emoji = self._get_gesture_emoji(gesture_name)
            cv2.putText(frame, f"Gesture: {gesture_name} {emoji} ({confidence}%)", (10, 70),
                      cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            # For debugging - show if this gesture is a toggle action
            is_toggle = gesture_name in ["Open_Palm", "ILoveYou"]
            can_toggle = time.time() - self.last_toggle_time > 1.5
            cv2.putText(frame, f"Toggle ready: {'Yes' if (is_toggle and can_toggle) else 'No'}", 
                      (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            
            # Check if gesture has changed
            if gesture_name != self.previous_gesture:
                self.previous_gesture = gesture_name
                self.gesture_start_time = time.time()
            
            # Only execute gesture if it's stable for a short time and has high confidence
            if gesture_score > 0.65 and time.time() - self.gesture_start_time > 0.3:  # Lower confidence threshold
                if self._should_execute_gesture(gesture_name):
                    self._execute_gesture_action(gesture_name)
                    print(f"🎯 Gesture: {gesture_name} {emoji} ({confidence}%)")
                return frame, gesture_name
                    
        except Exception as e:
            print(f"Error processing frame: {e}")
            cv2.putText(frame, "Error: " + str(e)[:30], (10, 130), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                
        return frame, None
    
    def _draw_landmarks(self, frame, hand_landmarks):
        """
        Draw hand landmarks on the frame.
        
        Args:
            frame: The image frame to draw on
            hand_landmarks: Hand landmarks from MediaPipe Tasks API
        """
        # Convert landmarks to the format expected by mp_drawing.draw_landmarks
        height, width, _ = frame.shape
        landmarks_list = []
        
        # Draw each landmark as a circle
        for landmark in hand_landmarks:
            # Convert normalized coordinates to pixel coordinates
            x = int(landmark.x * width)
            y = int(landmark.y * height)
            
            # Draw a small circle for each landmark
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
            
            # Store landmarks for connection drawing
            landmarks_list.append((x, y))
        
        # Draw connections between landmarks to form the hand skeleton
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),  # Thumb
            (0, 5), (5, 6), (6, 7), (7, 8),  # Index finger
            (0, 9), (9, 10), (10, 11), (11, 12),  # Middle finger
            (0, 13), (13, 14), (14, 15), (15, 16),  # Ring finger
            (0, 17), (17, 18), (18, 19), (19, 20),  # Pinky
            (5, 9), (9, 13), (13, 17)  # Palm
        ]
        
        # Draw the connections
        for connection in connections:
            start_idx, end_idx = connection
            if start_idx < len(landmarks_list) and end_idx < len(landmarks_list):
                cv2.line(frame, landmarks_list[start_idx], landmarks_list[end_idx], (255, 255, 255), 2)
    
    def _get_gesture_emoji(self, gesture_name):
        """Return emoji for the given gesture name."""
        emoji_map = {
            "Thumb_Up": "👍",
            "Thumb_Down": "👎",
            "Open_Palm": "👋",
            "Closed_Fist": "✊",
            "Victory": "✌️",
            "Pointing_Up": "☝️",
            "ILoveYou": "🤟"
        }
        return emoji_map.get(gesture_name, "")
    
    def _should_execute_gesture(self, gesture_name):
        """
        Determine if a gesture should trigger an action based on timing.
        
        Args:
            gesture_name: Detected gesture name
            
        Returns:
            bool: True if action should be executed
        """
        current_time = time.time()
        
        # For toggle actions (play/pause, mute), enforce longer cooldown
        if gesture_name in ["Open_Palm", "ILoveYou"]:
            if current_time - self.last_toggle_time > 1.5:
                self.last_toggle_time = current_time
                return True
            return False
            
        # For all other gestures, use normal cooldown
        if current_time - self.last_gesture_time < GESTURE_COOLDOWN:
            return False
            
        self.last_gesture_time = current_time
        return True
        
    def _execute_gesture_action(self, gesture_name):
        """
        Execute action based on detected gesture using VLC media player controls.
        
        Args:
            gesture_name: MediaPipe's gesture name
        """
        # VLC specific actions based on the 7 MediaPipe gestures
        if gesture_name == "Open_Palm":  # 👋
            # Try both space and 'k' for play/pause in VLC
            try:
                print("Sending play/pause command (space)")
                pyautogui.press("space")
            except Exception as e:
                print(f"Error sending space key: {e}")
                
            print("Action: Toggle Play/Pause")
            
        elif gesture_name == "ILoveYou":  # 🤟
            pyautogui.press("m")  # Mute in VLC
            print("Action: Toggle Mute")
            
        elif gesture_name == "Thumb_Up":  # 👍
            pyautogui.press("right")  # Seek forward in VLC
            print("Action: Seek Forward")
            
        elif gesture_name == "Thumb_Down":  # 👎
            pyautogui.press("left")  # Seek backward in VLC
            print("Action: Seek Backward")
            
        elif gesture_name == "Victory":  # ✌️
            pyautogui.hotkey('shift', 's')  # Screenshot in VLC
            print("Action: Screenshot")
            
        elif gesture_name == "Pointing_Up":  # ☝️
            self.audio_controller.increase_volume(VOLUME_SENSITIVITY)  # Volume up
            print("Action: Volume Up")
            
        elif gesture_name == "Closed_Fist":  # ✊
            self.audio_controller.decrease_volume(VOLUME_SENSITIVITY)  # Volume down
            print("Action: Volume Down")

