import pyaudio
import wave
import requests
import json
from datetime import datetime
import os
from typing import Optional, Dict, List
from PyQt5.QtCore import QThread, pyqtSignal

from .config import (
    SAMPLE_RATE, BIT_DEPTH, CHANNELS, MAX_FILE_SIZE, RECORD_TIME,
    SHAZAM_API_KEY, SHAZAM_API_HOST, SHAZAM_API_ENDPOINT
)

class AudioManager(QThread):
    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)
    recording_finished = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.is_recording = False
        self.playlists = self.load_playlists()

    def load_playlists(self) -> Dict[str, List[dict]]:
        """Load playlists from file"""
        if os.path.exists('playlists.json'):
            try:
                with open('playlists.json', 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading playlists: {e}")
        return {
            'happiness': [],
            'emotional': [],
            'relaxation': [],
            'excitement': []
        }

    def save_playlists(self):
        """Save playlists to file"""
        try:
            with open('playlists.json', 'w') as f:
                json.dump(self.playlists, f, indent=2)
        except Exception as e:
            print(f"Error saving playlists: {e}")

    def add_to_playlist(self, song: dict, playlist_id: str) -> bool:
        """Add a song to a playlist"""
        if playlist_id in self.playlists:
            # Check if song already exists
            for existing_song in self.playlists[playlist_id]:
                if (existing_song['title'] == song['title'] and 
                    existing_song['artist'] == song['artist']):
                    return False
            
            self.playlists[playlist_id].append(song)
            self.save_playlists()
            return True
        return False

    def get_playlist(self, playlist_id: str) -> List[dict]:
        """Get songs from a playlist"""
        return self.playlists.get(playlist_id, [])

    def start_recording(self):
        """Start the recording process"""
        self.is_recording = True
        self.start()

    def stop_recording(self):
        """Stop the recording process"""
        self.is_recording = False

    def get_input_device_index(self) -> Optional[int]:
        """Find the system audio input device"""
        p = pyaudio.PyAudio()
        try:
            # Look for a loopback device
            for i in range(p.get_device_count()):
                device_info = p.get_device_info_by_index(i)
                if 'loopback' in device_info['name'].lower():
                    return i
                
            # If no loopback device found, try to find system audio input
            for i in range(p.get_device_count()):
                device_info = p.get_device_info_by_index(i)
                if device_info['maxInputChannels'] > 0:
                    print(f"Using input device: {device_info['name']}")
                    return i
        finally:
            p.terminate()
        return None

    def record_audio(self) -> Optional[str]:
        """Record system audio"""
        p = pyaudio.PyAudio()
        device_index = self.get_input_device_index()
        
        if device_index is None:
            print("No suitable audio input device found")
            return None

        try:
            stream = p.open(
                format=pyaudio.paInt16,
                channels=CHANNELS,
                rate=SAMPLE_RATE,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=1024
            )

            frames = []
            chunks_to_record = int(SAMPLE_RATE / 1024 * RECORD_TIME)
            
            for i in range(chunks_to_record):
                if not self.is_recording:
                    break
                    
                data = stream.read(1024, exception_on_overflow=False)
                frames.append(data)
                progress = (i / chunks_to_record) * 100
                self.progress_updated.emit(int(progress))

            stream.stop_stream()
            stream.close()
            p.terminate()

            if not frames:
                return None

            # Save as WAV file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recording_{timestamp}.wav"
            
            wf = wave.open(filename, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

            return filename
            
        except Exception as e:
            print(f"Error recording audio: {e}")
            if 'stream' in locals():
                stream.close()
            p.terminate()
            return None

    def recognize_song(self, audio_file: str) -> Optional[dict]:
        """Send audio to Shazam API for recognition"""
        try:
            with open(audio_file, 'rb') as f:
                files = {
                    'upload_file': (audio_file, f, 'audio/wav')
                }
                headers = {
                    'x-rapidapi-key': SHAZAM_API_KEY,
                    'x-rapidapi-host': SHAZAM_API_HOST
                }
                response = requests.post(
                    SHAZAM_API_ENDPOINT,
                    headers=headers,
                    files=files
                )
            
            # Clean up the audio file
            os.remove(audio_file)
            
            if response.status_code == 200:
                result = response.json()
                if result and 'track' in result:
                    track = result['track']
                    return {
                        'title': track.get('title', 'Unknown'),
                        'artist': track.get('subtitle', 'Unknown'),
                        'key': track.get('key', '')
                    }
            
            print(f"API Response: {response.text}")
            return None
            
        except Exception as e:
            print(f"Error recognizing song: {e}")
            return None

    def run(self):
        """Run the recording process"""
        self.status_updated.emit("Initializing audio...")
        
        # Record audio
        audio_file = self.record_audio()
        if not audio_file:
            self.recording_finished.emit({'error': 'Recording failed'})
            return
        
        self.status_updated.emit("Processing audio...")
        
        # Recognize song
        song = self.recognize_song(audio_file)
        if song:
            self.recording_finished.emit({'song': song})
        else:
            self.recording_finished.emit({'error': 'Recognition failed'})
