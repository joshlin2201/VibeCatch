# VibeCatch 🎵

VibeCatch is a modern song recognition application that helps you organize music into mood-based playlists. It offers both command-line and graphical interfaces.

## Features

- 🎯 **Real-time Song Recognition**: Uses Shazam's API for accurate music detection
- 🎭 **Mood-Based Playlists**: Organize songs into different vibes:
  - Get Hyped: High-energy tracks
  - Chill Vibes: Relaxing tunes
  - Romantic Feels: Love and emotional songs
  - Focus Mode: Concentration-enhancing tracks
  - Feel-Good Tunes: Uplifting music
- 🎨 **Multiple Interfaces**: Choose between CLI or modern GUI
- 🎤 **Smart Audio Detection**: Advanced audio processing for reliable song detection
- 💾 **Persistent Storage**: Automatically saves your playlists

## Installation

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

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. System-specific requirements:
   - **macOS**: `brew install portaudio`
   - **Linux**: `sudo apt-get install python3-pyaudio portaudio19-dev`
   - **Windows**: No additional steps needed

## Usage

### Command Line Interface (CLI)

Run the CLI version:
```bash
python vibecatch.py
```

- Press Enter to start listening
- Wait for song recognition
- Choose a playlist to add the song to
- View your organized playlists

### Graphical Interface (GUI)

Run the GUI version:
```bash
python gui_app.py
```

Features:
- Modern, dark-themed interface
- Real-time progress visualization
- Easy playlist management
- Click-to-record functionality
- Visual song organization

## Technical Details

### Audio Processing
- 44.1kHz sample rate
- 16-bit audio depth
- Mono channel recording
- Advanced audio level detection
- Automatic gain control

### API Integration
- Uses Shazam API via RapidAPI
- Optimized for quick recognition
- Handles various audio formats
- Robust error handling

### GUI Features
- Built with PyQt5
- Modern Dracula-inspired theme
- Responsive design
- Thread-safe audio processing
- Real-time visual feedback

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Shazam API via RapidAPI for song recognition
- PyQt5 for the graphical interface
- Dracula theme for color inspiration
- Modern GUI Template by anjalp for design inspiration
