import pyaudio
import wave
import time
import requests
import json
from datetime import datetime
import os
from typing import Dict, List, Optional
import numpy as np

class VibeCatch:
    def __init__(self):
        # Audio settings matching WhatAmIHearing
        self.SAMPLE_RATE = 44100
        self.CHANNELS = 1
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.MAX_BYTES = 500 * 1000  # 500KB max for Shazam API
        self.RECORD_SECONDS = 5
        
        # API settings
        self.API_KEY = 'fa5a6a869emsha1e5c0d55e85365p18dc1djsnd0540648d450'
        self.API_HOST = 'shazam-api6.p.rapidapi.com'
        
        # Playlist management
        self.playlists: Dict[str, List[dict]] = {
            'hyped': [],
            'chill': [],
            'romantic': [],
            'focus': [],
            'feelgood': []
        }
        
        # Load existing playlists if available
        if os.path.exists('playlists.json'):
            try:
                with open('playlists.json', 'r') as f:
                    self.playlists = json.load(f)
            except:
                pass

    def get_input_device_index(self):
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
        print("\nInitializing audio capture...")
        
        p = pyaudio.PyAudio()
        device_index = self.get_input_device_index()
        
        if device_index is None:
            print("No suitable audio input device found")
            return None

        try:
            stream = p.open(format=self.FORMAT,
                          channels=self.CHANNELS,
                          rate=self.SAMPLE_RATE,
                          input=True,
                          input_device_index=device_index,
                          frames_per_buffer=self.CHUNK)

            print("\nRecording system audio...")
            frames = []
            
            for i in range(0, int(self.SAMPLE_RATE / self.CHUNK * self.RECORD_SECONDS)):
                data = stream.read(self.CHUNK, exception_on_overflow=False)
                frames.append(data)
                progress = (i / (self.SAMPLE_RATE / self.CHUNK * self.RECORD_SECONDS)) * 100
                print(f'\rRecording progress: {progress:.1f}%', end='')

            print("\nFinished recording")

            stream.stop_stream()
            stream.close()
            p.terminate()

            # Save as WAV file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recording_{timestamp}.wav"
            
            wf = wave.open(filename, 'wb')
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(p.get_sample_size(self.FORMAT))
            wf.setframerate(self.SAMPLE_RATE)
            wf.writeframes(b''.join(frames))
            wf.close()

            return filename
            
        except Exception as e:
            print(f"\nError recording audio: {e}")
            if 'stream' in locals():
                stream.close()
            p.terminate()
            return None

    def recognize_song(self, audio_file: str) -> Optional[dict]:
        """Send audio to Shazam API for recognition"""
        print("\nSending to Shazam API...")
        
        url = "https://shazam-api6.p.rapidapi.com/shazam/recognize/"
        headers = {
            "x-rapidapi-key": self.API_KEY,
            "x-rapidapi-host": self.API_HOST
        }

        try:
            with open(audio_file, 'rb') as f:
                files = {
                    'upload_file': (audio_file, f, 'audio/wav')
                }
                response = requests.post(url, headers=headers, files=files)
            
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

    def suggest_playlist(self, song: dict) -> List[str]:
        """Suggest playlists based on song characteristics"""
        # In a full implementation, this would analyze the song's tempo, energy, etc.
        # For MVP, we'll return all playlists for user selection
        return list(self.playlists.keys())

    def add_to_playlist(self, song: dict, playlist_name: str) -> bool:
        """Add a song to a specific playlist"""
        if playlist_name in self.playlists:
            # Check if song already exists in playlist
            for existing_song in self.playlists[playlist_name]:
                if existing_song['title'] == song['title'] and existing_song['artist'] == song['artist']:
                    print(f"\nSong already exists in {playlist_name} playlist!")
                    return False
            
            self.playlists[playlist_name].append(song)
            # Save playlists after each addition
            with open('playlists.json', 'w') as f:
                json.dump(self.playlists, f, indent=2)
            return True
        return False

    def show_playlists(self):
        """Display all playlists and their songs"""
        print("\nCurrent Playlists:")
        print("------------------")
        for name, songs in self.playlists.items():
            if songs:
                print(f"\n{name.upper()} Playlist:")
                for i, song in enumerate(songs, 1):
                    print(f"{i}. {song['title']} - {song['artist']}")

    def run(self):
        """Main recognition loop"""
        print("VibeCatch Song Recognizer")
        print("-------------------------")
        print("Make sure your system audio is playing clearly.")
        
        try:
            while True:
                input("\nPress Enter to start listening (or Ctrl+C to exit)...")
                
                # Record audio
                audio_file = self.record_audio()
                if not audio_file:
                    continue
                
                # Recognize song
                song = self.recognize_song(audio_file)
                
                if song:
                    print("\nSong recognized!")
                    print(f"Title: {song['title']}")
                    print(f"Artist: {song['artist']}")
                    
                    # Show playlist options
                    print("\nAdd to playlist:")
                    playlists = self.suggest_playlist(song)
                    for i, playlist in enumerate(playlists, 1):
                        print(f"{i}. {playlist}")
                    
                    try:
                        choice = int(input("\nSelect playlist number (or 0 to skip): "))
                        if 0 < choice <= len(playlists):
                            playlist_name = playlists[choice - 1]
                            if self.add_to_playlist(song, playlist_name):
                                print(f"\nAdded to {playlist_name} playlist!")
                                self.show_playlists()
                    except ValueError:
                        print("Invalid selection, skipping...")
                else:
                    print("\nCouldn't recognize the song. Please try again.")

        except KeyboardInterrupt:
            print("\nExiting...")

if __name__ == "__main__":
    app = VibeCatch()
    app.run()
