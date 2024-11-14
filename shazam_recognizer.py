import pyaudio
import wave
import time
import requests
from datetime import datetime
import os

class ShazamRecognizer:
    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.RECORD_SECONDS = 5
        self.MAX_FILE_SIZE = 500 * 1000  # 500KB max
        self.API_KEY = 'fa5a6a869emsha1e5c0d55e85365p18dc1djsnd0540648d450'
        self.API_HOST = 'shazam-api6.p.rapidapi.com'

    def record_audio(self):
        """Record audio from microphone"""
        print("\nInitializing audio...")
        p = pyaudio.PyAudio()

        # Open stream
        stream = p.open(format=self.FORMAT,
                       channels=self.CHANNELS,
                       rate=self.RATE,
                       input=True,
                       frames_per_buffer=self.CHUNK)

        print("Recording...")
        frames = []

        # Record audio
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            frames.append(data)
            # Print progress
            progress = (i / (self.RATE / self.CHUNK * self.RECORD_SECONDS)) * 100
            print(f"Recording progress: {progress:.1f}%", end='\r')

        print("\nFinished recording")

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Save the recorded data as a WAV file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"recording_{timestamp}.wav"
        
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        return filename

    def recognize_song(self, audio_file):
        """Send audio to Shazam API for recognition"""
        print("\nSending to Shazam API...")
        
        url = "https://shazam-api6.p.rapidapi.com/shazam/recognize/"
        
        headers = {
            "x-rapidapi-key": self.API_KEY,
            "x-rapidapi-host": self.API_HOST
        }

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
            else:
                print("No song detected")
                return None
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return None

    def run(self):
        """Main recognition loop"""
        try:
            while True:
                input("\nPress Enter to start listening (or Ctrl+C to exit)...")
                
                # Record audio
                audio_file = self.record_audio()
                
                # Recognize song
                result = self.recognize_song(audio_file)
                
                if result:
                    print("\nSong recognized!")
                    print(f"Title: {result['title']}")
                    print(f"Artist: {result['artist']}")
                else:
                    print("\nCouldn't recognize the song. Please try again.")

        except KeyboardInterrupt:
            print("\nExiting...")

if __name__ == "__main__":
    print("VibeCatch Song Recognizer")
    print("-------------------------")
    print("Make sure your microphone is ready and music is playing clearly.")
    
    recognizer = ShazamRecognizer()
    recognizer.run()
