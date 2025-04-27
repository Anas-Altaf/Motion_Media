"""
Voice recognition for media player control.
"""
import pyautogui
import speech_recognition as sr


class VoiceController:
    """
    Controls media player based on voice commands.
    """
    def __init__(self, audio_controller):
        """
        Initialize the voice controller.
        
        Args:
            audio_controller: Instance of AudioController for volume control
        """
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.audio_controller = audio_controller
        
    def listen_for_commands(self):
        """
        Listen for voice commands and execute corresponding actions.
        
        Returns:
            str or None: Recognized command or None if no command recognized
        """
        try:
            with self.mic as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("ing for commands...")
                audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=3)
                
            command = self.recognizer.recognize_google(audio).lower()
            print(f"Detected command: {command}")
            
            self._execute_command(command)
            return command
            
        except (sr.UnknownValueError, sr.WaitTimeoutError):
            return None
        except Exception as e:
            print(f"Voice recognition error: {e}")
            return None
    
    def _execute_command(self, command):
        """Execute actions based on recognized voice command."""
        if "play" in command or "pause" in command:
            pyautogui.press("space")
        elif "volume" in command:
            if "up" in command:
                self.audio_controller.increase_volume(0.2)
            elif "down" in command:
                self.audio_controller.decrease_volume(0.2)
        elif "skip" in command or "forward" in command:
            pyautogui.press("right")
        elif "back" in command or "previous" in command:
            pyautogui.press("left")
        elif "mute" in command:
            pyautogui.press("m")
