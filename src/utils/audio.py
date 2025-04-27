"""
Audio utilities for volume control.
"""
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class AudioController:
    """
    Controls system audio volume using the pycaw library.
    """
    def __init__(self):
        """Initialize the audio controller."""
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume_interface = cast(interface, POINTER(IAudioEndpointVolume))
        self.current_volume = self.volume_interface.GetMasterVolumeLevelScalar()

    def get_volume(self):
        """Get the current volume level."""
        self.current_volume = self.volume_interface.GetMasterVolumeLevelScalar()
        return self.current_volume
        
    def set_volume(self, new_level):
        """
        Set the system volume level.
        
        Args:
            new_level (float): Volume level between 0.0 and 1.0
        """
        new_level = max(0.0, min(1.0, new_level))  # Ensure volume level is between 0 and 1
        self.volume_interface.SetMasterVolumeLevelScalar(new_level, None)
        self.current_volume = new_level
        
    def increase_volume(self, increment=0.1):
        """
        Increase the system volume.
        
        Args:
            increment (float): Amount to increase volume by (0.0-1.0)
        """
        self.set_volume(self.get_volume() + increment)
        
    def decrease_volume(self, decrement=0.1):
        """
        Decrease the system volume.
        
        Args:
            decrement (float): Amount to decrease volume by (0.0-1.0)
        """
        self.set_volume(self.get_volume() - decrement)
