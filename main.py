"""
Main module for the Gesture Media Controller application.
"""
import cv2
import time

from src.config import DEFAULT_CONTROL_MODES
from src.utils.audio import AudioController
from src.controllers.gesture_controller import GestureController
from src.controllers.face_controller import FaceController
from src.controllers.voice_controller import VoiceController


class MediaController:
    """
    Main class that integrates all controller modules.
    """
    def __init__(self):
        """Initialize the media controller with all sub-controllers."""
        # Initialize audio controller first as it's needed by other controllers
        self.audio_controller = AudioController()
        
        # Initialize the specific controllers
        self.gesture_controller = GestureController(self.audio_controller)
        self.face_controller = FaceController()
        self.voice_controller = VoiceController(self.audio_controller)
        
        # Control mode settings
        self.control_modes = DEFAULT_CONTROL_MODES.copy()
        
    def run(self):
        """
        Run the main application loop.
        """
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open video capture device.")
            return
            
        print("Starting Media Controller...")
        print("Press 'q' to quit, 'g' to toggle gesture control,")
        print("'f' to toggle face control, 'v' to toggle voice control.")
        
        running = True
        while running and cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture frame.")
                break
                
            # Flip frame horizontally for a mirror effect
            frame = cv2.flip(frame, 1)
            
            # Process with active controllers
            if self.control_modes["gesture"]:
                frame, gesture = self.gesture_controller.process_frame(frame)
            
            if self.control_modes["face"]:
                frame, _ = self.face_controller.process_frame(frame)
                
            if self.control_modes["voice"]:
                self.voice_controller.listen_for_commands()
                
            # Display control mode status
            self._display_status(frame)
            
            # Show the frame
            cv2.imshow('Media Controller', frame)
            
            # Handle keyboard input
            running = self._handle_keyboard_input()
                
        # Cleanup
        cap.release()
        cv2.destroyAllWindows()
    
    def _display_status(self, frame):
        """Display the status of each control mode in the bottom-left corner of the frame."""
        status_text = [
            f"Gesture: {'ON' if self.control_modes['gesture'] else 'OFF'}",
            f"Face: {'ON' if self.control_modes['face'] else 'OFF'}",
            f"Voice: {'ON' if self.control_modes['voice'] else 'OFF'}"
        ]
        
        # Get frame height
        height, _, _ = frame.shape
        
        # Calculate starting y-position from bottom
        # Leave a margin of 30 pixels from the bottom
        base_y_position = height - 30
        
        # Draw text from bottom up (reverse order)
        for i, text in enumerate(reversed(status_text)):
            y_position = base_y_position - i*30
            cv2.putText(frame, text, (10, y_position), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    def _handle_keyboard_input(self):
        """
        Handle keyboard input for toggling modes and quitting.
        
        Returns:
            bool: False if the application should quit, True otherwise
        """
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            return False  # Signal to quit
        elif key == ord('g'):
            self.control_modes["gesture"] = not self.control_modes["gesture"]
        elif key == ord('f'):
            self.control_modes["face"] = not self.control_modes["face"]
        elif key == ord('v'):
            self.control_modes["voice"] = not self.control_modes["voice"]
        return True


def run():
    """Entry point function for the application."""
    controller = MediaController()
    controller.run()


if __name__ == "__main__":
    run()
