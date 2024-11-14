# VibeCatch 🎵

A modern song recognition application that helps you organize music into scientifically-backed mood-based playlists.

## Features

- 🎯 **Real-time Song Recognition**: Uses Shazam's API for accurate music detection
- 🧠 **Science-Based Vibes**: Four core emotional categories based on music research:
  - **Happiness and Joy**: Upbeat tempos and major keys activate dopamine and serotonin
  - **Emotional Depth**: Minor keys and slower tempos for introspection
  - **Relaxation and Calm**: Gentle rhythms to lower cortisol levels
  - **Excitement and Energy**: Fast-paced beats for enhanced motivation
- 🎨 **Modern Interface**: Clean, intuitive design with real-time feedback
- 💾 **Persistent Storage**: Automatically saves your playlists

## Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/vibecatch.git
   cd vibecatch
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the package:
   ```bash
   pip install -e .
   ```

4. System-specific requirements:
   - **macOS**: `brew install portaudio`
   - **Linux**: `sudo apt-get install python3-pyaudio portaudio19-dev`
   - **Windows**: No additional steps needed

## Usage

1. Start the application:
   ```bash
   python -m vibecatch
   ```

2. Using the application:
   - Click "Start Listening" to begin recording
   - Wait for song recognition (5 seconds)
   - Choose a mood-based playlist to add the song
   - View your organized playlists
   - Use the "Copy" button to copy playlist contents to clipboard

## Project Structure

```
src/vibecatch/
├── core/               # Core functionality
│   ├── audio_manager.py   # Audio recording and recognition
│   └── config.py          # Application configuration
├── styles/             # UI styling
│   ├── colors.py         # Color definitions
│   └── components.py     # Component styles
├── ui/                 # User interface components
│   ├── main_window.py    # Main application window
│   ├── playlist_widget.py # Playlist component
│   └── record_widget.py  # Recording interface
└── __main__.py        # Application entry point
```

## Data Storage

The application maintains persistent storage for playlists and temporary audio recordings:

- **Playlists**: Stored in `src/vibecatch/data/playlists.json`
  - Automatically created if it doesn't exist
  - Each playlist is categorized by mood
  - Songs are stored with title, artist, and unique identifier
  - Changes are saved immediately after modifications

- **Recordings**: Temporarily stored in `src/vibecatch/data/recordings/`
  - WAV format audio files
  - Named with timestamps for uniqueness
  - Automatically cleaned up after song recognition

## Understanding the Setup

This section explains the installation process in detail, particularly helpful for beginners.

### Virtual Environment Setup
The command `python -m venv venv` followed by activation is a crucial step. Here's why:

- **What is a virtual environment?**
  - Think of it as a clean, isolated room for your project
  - Prevents conflicts between different Python projects on your computer
  - Each project can have its own versions of packages
  - Makes sharing your project easier as others can recreate the exact same environment

- **Command Breakdown:**
  - `python -m venv venv`: Creates a new virtual environment named "venv"
  - `source venv/bin/activate` or `venv\Scripts\activate`: Activates the environment
  - When activated, you'll see `(venv)` at the start of your command prompt
  - To deactivate later, simply type `deactivate`

### Package Installation
The command `pip install -e .` sets up the project. Here's what it does:

- **Command Explanation:**
  - `pip` is Python's package installer
  - `-e` means "editable" installation
  - `.` means "install from the current directory"

- **What happens during installation:**
  - Reads the `setup.py` file
  - Installs all required dependencies
  - Sets up the project in development mode
  - Allows you to modify code without reinstalling

- **Why development mode (-e)?**
  - Changes to the code take effect immediately
  - No need to reinstall after making changes
  - Perfect for development and testing

## Development

### Requirements
- Python 3.8+
- PyQt5
- PyAudio
- Requests

### Running Tests
```bash
python -m pytest tests/
```

### Building from Source
```bash
python setup.py build
```

## Technical Details

### Audio Processing
- 44.1kHz sample rate
- 16-bit audio depth
- Mono channel recording
- 500KB maximum file size
- WAV format for high quality

### API Integration
- Shazam API via RapidAPI
- Real-time song recognition
- Robust error handling
- Automatic cleanup of temporary files

### UI Features
- Modern Dracula-inspired theme
- Responsive design
- Thread-safe audio processing
- Real-time visual feedback
- Efficient playlist management
- Interactive copy functionality with visual feedback

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Shazam API via RapidAPI for song recognition
- PyQt5 for the graphical interface
- Dracula theme for color inspiration
- Music psychology research for vibe categorization
