"""
Face detection for automatic media playback control.
"""
import cv2
import mediapipe as mp
import pyautogui


class FaceController:
    """
    Controls media player based on face detection.
    """
    def __init__(self):
        """Initialize the face controller."""
        self.mp_face = mp.solutions.face_detection
        self.face_detector = self.mp_face.FaceDetection(min_detection_confidence=0.5)
        self.prev_face_state = True  # Assume face is initially detected
        
    def process_frame(self, frame):
        """
        Process a video frame to detect faces.
        
        Args:
            frame: OpenCV image frame
            
        Returns:
            processed_frame: Frame with face detection drawn
            face_state_changed: True if face state changed, False otherwise
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_results = self.face_detector.process(frame_rgb)
        
        face_detected = face_results.detections is not None and len(face_results.detections) > 0
        face_state_changed = self._handle_face_state(face_detected)
        
        # Draw face detection box if face detected
        if face_detected:
            frame = self._draw_face_box(frame, face_results.detections)
            
        return frame, face_state_changed
        
    def _handle_face_state(self, face_detected):
        """
        Handle changes in face detection state.
        
        Args:
            face_detected: Whether a face is currently detected
            
        Returns:
            bool: True if state changed, False otherwise
        """
        if face_detected != self.prev_face_state:
            if face_detected:
                print("Face detected - resuming playback")
            else:
                print("Face lost - pausing playback")
            pyautogui.press("space")
            self.prev_face_state = face_detected
            return True
        return False
        
    def _draw_face_box(self, frame, detections):
        """Draw boxes around detected faces."""
        for detection in detections:
            bbox = detection.location_data.relative_bounding_box
            ih, iw, _ = frame.shape
            x, y = int(bbox.xmin * iw), int(bbox.ymin * ih)
            w, h = int(bbox.width * iw), int(bbox.height * ih)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        return frame
