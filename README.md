# 🎮 Motion Media Controller

A Python application that allows you to control media players using hand gestures, face detection, and voice commands.

## 📋 Table of Contents
- ✨ Features
- 🛠️ Installation
- 📖 Usage
- 🖐️ Gesture Controls
- 👤 Face Detection
- 🎤 Voice Commands
- ⚙️ Configuration
- 🧩 Project Structure
- 🚀 Future Enhancements
- 📄 License

## ✨ Features

- **🖐️ Gesture Control**: Control your media player with hand gestures
  - Open Palm (👋): Play/Pause
  - Thumbs Up (👍): Seek Forward
  - Thumbs Down (👎): Seek Backward
  - ILoveYou Sign (🤟): Toggle Mute
  - Victory Sign (✌️): Take Screenshot
  - Pointing Up (☝️): Volume Up
  - Closed Fist (✊): Volume Down

- **👤 Face Detection**: Auto-pause when you look away from the screen

- **🎤 Voice Commands**: Control playback using natural voice commands

## 🛠️ Installation

### Using Poetry (recommended)

```bash
# Clone the repository
git clone https://github.com/Anas-Altaf/Motion_Media.git
cd Motion_Media

# Install dependencies with Poetry
poetry install

# Run the application
poetry run python -m src.main
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/Anas-Altaf/Motion_Media.git
cd Motion_Media

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m src.main
```

## 📖 Usage

1. Start the application using one of the methods above
2. Ensure your webcam is properly connected and accessible
3. Position yourself in front of the camera
4. Use the keyboard shortcuts to enable/disable control modes:
   - `q`: Quit the application
   - `g`: Toggle gesture control on/off
   - `f`: Toggle face control on/off
   - `v`: Toggle voice control on/off
5. Control your media player with the supported gestures, face detection, or voice commands

## 🖐️ Gesture Controls

| Gesture | Icon | Action | Description |
|---------|------|--------|-------------|
| Open Palm | 👋 | Play/Pause | Show an open palm to toggle between play and pause |
| Thumbs Up | 👍 | Seek Forward | Give a thumbs up to seek forward in the media |
| Thumbs Down | 👎 | Seek Backward | Give a thumbs down to seek backward in the media |
| ILoveYou | 🤟 | Toggle Mute | Make the ILoveYou sign to mute/unmute audio |
| Victory | ✌️ | Screenshot | Make a victory sign to take a screenshot |
| Pointing Up | ☝️ | Volume Up | Point upward to increase volume |
| Closed Fist | ✊ | Volume Down | Make a fist to decrease volume |

## 👤 Face Detection

When face control is enabled, the application:
- Monitors your presence in front of the camera
- Auto-pauses media when you look away or leave
- Auto-resumes playback when you return (only if it was paused by face detection)

## 🎤 Voice Commands

When voice control is enabled, you can use these commands:
- "Play" or "Pause" - Toggle play/pause
- "Volume up" - Increase volume
- "Volume down" - Decrease volume
- "Skip" or "Forward" - Seek forward
- "Back" or "Previous" - Seek backward
- "Mute" - Toggle mute/unmute

## ⚙️ Configuration

The default configuration settings are in config.py:
- `GESTURE_THRESHOLD`: Threshold for gesture detection sensitivity
- `VOLUME_SENSITIVITY`: How much each volume change action affects the volume
- `GESTURE_COOLDOWN`: Time between gesture detections to prevent accidental triggers
- `DEFAULT_CONTROL_MODES`: Which control modes are enabled by default

## 🧩 Project Structure

```
Motion_Media/
├── pyproject.toml       # Poetry configuration
├── README.md           # Project documentation
├── src/                # Source code
│   ├── __init__.py
│   ├── main.py         # Entry point
│   ├── config.py       # Configuration settings
│   ├── controllers/    # Input controller modules
│   │   ├── gesture_controller.py
│   │   ├── face_controller.py
│   │   ├── voice_controller.py
│   │   └── __init__.py
│   └── utils/          # Utility modules
│       ├── audio.py    # Audio control utilities
│       └── __init__.py
├── models/             # Pre-trained ML models
│   └── gesture_recognizer.task
├── docs/               # Documentation
│   └── usage.md        # Detailed usage guide
└── tests/              # Test scripts
```

## 🚀 Future Enhancements

- Custom gesture mapping for personalized controls
- Support for additional media players
- Mobile app integration for remote control
- REST API for external application integration
- Improved gesture detection accuracy
- Accessibility features for users with different needs

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Made with ❤️ by [Anas Altaf](https://github.com/Anas-Altaf)