# Gesture Media Controller

A Python application that allows controlling media players using gestures, face detection, and voice commands.

## Features

- **Gesture Control**: Use hand gestures to control media playback
  - Open palm: Play/Pause
  - Thumbs up: Volume Up
  - Thumbs down: Volume Down
  - Pinch: Seek through media
- **Face Detection**: Auto-pause when you look away from the screen
- **Voice Commands**: Control playback using voice
  - "Play/Pause": Toggle playback
  - "Volume up/down": Adjust volume
  - "Skip/Forward": Jump forward
  - "Back/Previous": Jump backward
  - "Mute": Mute audio

## Installation

### Using Poetry (recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/gesture-media-controller.git
cd gesture-media-controller

# Install dependencies with Poetry
poetry install

# Run the application
poetry run gesture-controller
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/gesture-media-controller.git
cd gesture-media-controller

# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install with pip
pip install .

# Run the application
python -m gesture_media_controller.main
```

## Requirements

- Python 3.8 or higher
- Webcam
- Microphone (for voice commands)

## Usage

1. Start the application using one of the methods above
2. Position yourself in front of the webcam
3. Use the following keyboard shortcuts:
   - Press `q` to quit
   - Press `g` to toggle gesture control
   - Press `f` to toggle face control
   - Press `v` to toggle voice control

## Project Structure

```
gesture_media_controller/
├── pyproject.toml       # Poetry configuration
├── README.md           # Project documentation
├── src/
│   └── gesture_media_controller/
│       ├── __init__.py
│       ├── main.py      # Entry point
│       ├── controllers/ # Input controller modules
│       ├── utils/       # Utility functions
│       └── config.py    # Configuration settings
├── assets/             # Sample media files
├── docs/               # Additional documentation
└── tests/              # Test scripts
```

## License

MIT License
