"""
Tests for the audio controller module.
"""
import unittest
from unittest.mock import MagicMock, patch

from gesture_media_controller.utils.audio import AudioController


class TestAudioController(unittest.TestCase):
    """Test cases for AudioController class."""
    
    @patch('gesture_media_controller.utils.audio.AudioUtilities')
    @patch('gesture_media_controller.utils.audio.cast')
    def setUp(self, mock_cast, mock_audio_utils):
        """Set up test fixtures."""
        # Mock the volume interface
        self.mock_volume = MagicMock()
        self.mock_volume.GetMasterVolumeLevelScalar.return_value = 0.5
        mock_cast.return_value = self.mock_volume
        
        # Create AudioController instance
        self.audio_controller = AudioController()
    
    def test_get_volume(self):
        """Test getting the current volume level."""
        self.mock_volume.GetMasterVolumeLevelScalar.return_value = 0.75
        volume = self.audio_controller.get_volume()
        self.assertEqual(volume, 0.75)
        self.assertEqual(self.audio_controller.current_volume, 0.75)
    
    def test_set_volume(self):
        """Test setting the volume level."""
        self.audio_controller.set_volume(0.6)
        self.mock_volume.SetMasterVolumeLevelScalar.assert_called_with(0.6, None)
        self.assertEqual(self.audio_controller.current_volume, 0.6)
    
    def test_set_volume_clamps_values(self):
        """Test that set_volume clamps values to 0.0-1.0 range."""
        # Test with value greater than 1.0
        self.audio_controller.set_volume(1.5)
        self.mock_volume.SetMasterVolumeLevelScalar.assert_called_with(1.0, None)
        self.assertEqual(self.audio_controller.current_volume, 1.0)
        
        # Test with value less than 0.0
        self.audio_controller.set_volume(-0.5)
        self.mock_volume.SetMasterVolumeLevelScalar.assert_called_with(0.0, None)
        self.assertEqual(self.audio_controller.current_volume, 0.0)
    
    def test_increase_volume(self):
        """Test increasing volume."""
        self.audio_controller.current_volume = 0.5
        self.audio_controller.increase_volume(0.2)
        self.mock_volume.SetMasterVolumeLevelScalar.assert_called_with(0.7, None)
    
    def test_decrease_volume(self):
        """Test decreasing volume."""
        self.audio_controller.current_volume = 0.5
        self.audio_controller.decrease_volume(0.2)
        self.mock_volume.SetMasterVolumeLevelScalar.assert_called_with(0.3, None)


if __name__ == '__main__':
    unittest.main()
