# VibeCatch Song Recognizer

A simple song recognition tool that uses the Shazam API to identify songs playing through your microphone.

## Python Version Setup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Note: PyAudio might require additional system packages:
   - On macOS: `brew install portaudio`
   - On Ubuntu/Debian: `sudo apt-get install python3-pyaudio`
   - On Windows: No additional steps needed

2. Run the recognizer:
   ```bash
   python shazam_recognizer.py
   ```

3. Usage:
   - Press Enter to start listening
   - Play music clearly near your microphone
   - Wait for 5 seconds while it records
   - The program will attempt to identify the song
   - Press Ctrl+C to exit

## Features

- Real-time audio recording
- Integration with Shazam API for accurate song recognition
- Simple command-line interface
- 5-second recording window
- Progress indication during recording
- Automatic cleanup of temporary audio files

## Technical Details

- Records audio at 44.1kHz, 16-bit, mono
- Uses WAV format for high-quality audio capture
- Implements Shazam's 500KB file size limit
- Proper error handling and user feedback

## Requirements

- Python 3.6+
- PyAudio
- Requests

## Troubleshooting

If you encounter microphone issues:
1. Make sure your microphone is properly connected and selected as the default input device
2. Check your system's audio input settings
3. Ensure the music is playing clearly and loudly enough
4. Try running the program again

## License

MIT License - feel free to modify and use as needed.
