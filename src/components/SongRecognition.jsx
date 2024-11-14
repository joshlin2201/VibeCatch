import { useState, useRef, useEffect } from 'react';
import { 
  Box, 
  Button, 
  Card, 
  CardContent, 
  Typography,
  CircularProgress,
  Stack,
  LinearProgress
} from '@mui/material';
import axios from 'axios';
import { AudioDebugger } from '../utils/AudioDebugger';

const MOOD_PLAYLISTS = [
  { id: 'hyped', name: 'Get Hyped', color: '#FF4B4B' },
  { id: 'chill', name: 'Chill Vibes', color: '#4BCDFF' },
  { id: 'romantic', name: 'Romantic Feels', color: '#FF4BA6' },
  { id: 'focus', name: 'Focus Mode', color: '#8B4BFF' },
  { id: 'feelgood', name: 'Feel-Good Tunes', color: '#4BFF91' }
];

// Audio recording configuration
const SAMPLE_RATE = 44100;
const BIT_DEPTH = 16;
const CHANNELS = 1;
const MAX_FILE_SIZE = 500 * 1000; // 500KB max according to Shazam API
const RECORD_TIME = 5000; // 5 seconds in milliseconds

const SongRecognition = () => {
  const [isListening, setIsListening] = useState(false);
  const [recognizedSong, setRecognizedSong] = useState(null);
  const [error, setError] = useState(null);
  const [playlists, setPlaylists] = useState({});
  const [status, setStatus] = useState('');
  const [showPlaylistOptions, setShowPlaylistOptions] = useState(false);
  const [recordingProgress, setRecordingProgress] = useState(0);
  
  const mediaStream = useRef(null);
  const mediaRecorder = useRef(null);
  const recordedChunks = useRef([]);
  const progressInterval = useRef(null);
  const startTime = useRef(0);

  useEffect(() => {
    return () => stopListening();
  }, []);

  const initializeAudio = async () => {
    try {
      AudioDebugger.log('Init', 'Starting audio initialization');

      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          channelCount: CHANNELS,
          sampleRate: SAMPLE_RATE,
          sampleSize: BIT_DEPTH,
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true
        }
      });

      AudioDebugger.log('Init', 'Got media stream');
      await AudioDebugger.analyzeStream(stream);

      mediaStream.current = stream;
      mediaRecorder.current = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus',
        audioBitsPerSecond: SAMPLE_RATE * BIT_DEPTH
      });

      AudioDebugger.log('Init', 'MediaRecorder created', {
        state: mediaRecorder.current.state,
        mimeType: mediaRecorder.current.mimeType,
        bitrate: mediaRecorder.current.audioBitsPerSecond
      });

      recordedChunks.current = [];

      mediaRecorder.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          AudioDebugger.log('Recording', `Chunk received: ${event.data.size} bytes`);
          recordedChunks.current.push(event.data);
        }
      };

      mediaRecorder.current.onstop = async () => {
        AudioDebugger.log('Recording', 'MediaRecorder stopped');
        
        if (recordedChunks.current.length === 0) {
          setError('No audio data recorded. Please try again.');
          return;
        }

        const audioBlob = new Blob(recordedChunks.current, { type: 'audio/webm;codecs=opus' });
        AudioDebugger.logAudioData(audioBlob);

        if (audioBlob.size > MAX_FILE_SIZE) {
          AudioDebugger.log('Recording', 'Audio file too large, truncating');
          const truncatedBlob = audioBlob.slice(0, MAX_FILE_SIZE);
          await recognizeSongWithAPI(truncatedBlob);
        } else {
          await recognizeSongWithAPI(audioBlob);
        }
      };

      return true;
    } catch (err) {
      AudioDebugger.log('Error', 'Audio initialization failed', err);
      setError(`Microphone access error: ${err.message}`);
      return false;
    }
  };

  const stopListening = () => {
    AudioDebugger.log('Cleanup', 'Stopping recording');
    
    clearInterval(progressInterval.current);
    
    if (mediaRecorder.current?.state === 'recording') {
      mediaRecorder.current.stop();
    }

    if (mediaStream.current) {
      mediaStream.current.getTracks().forEach(track => {
        track.stop();
        AudioDebugger.log('Cleanup', `Track stopped: ${track.label}`);
      });
      mediaStream.current = null;
    }

    setIsListening(false);
    setStatus('');
    setRecordingProgress(0);
    recordedChunks.current = [];
    AudioDebugger.log('Cleanup', 'Complete');
  };

  const recognizeSongWithAPI = async (audioBlob) => {
    try {
      AudioDebugger.log('API', 'Preparing request');
      const formData = new FormData();
      formData.append('upload_file', audioBlob, 'recording.webm');

      AudioDebugger.log('API', 'Sending request to Shazam');
      const response = await axios({
        method: 'POST',
        url: 'https://shazam-api6.p.rapidapi.com/shazam/recognize/',
        headers: {
          'x-rapidapi-key': 'fa5a6a869emsha1e5c0d55e85365p18dc1djsnd0540648d450',
          'x-rapidapi-host': 'shazam-api6.p.rapidapi.com'
        },
        data: formData,
        maxContentLength: Infinity,
        maxBodyLength: Infinity
      });

      AudioDebugger.log('API', 'Response received', response.data);

      if (response.data && response.data.track) {
        setRecognizedSong({
          title: response.data.track.title,
          artist: response.data.track.subtitle,
          key: response.data.track.key
        });
        setShowPlaylistOptions(true);
        return true;
      } else {
        setError('Could not identify the song. Please try again.');
        return false;
      }
    } catch (err) {
      AudioDebugger.log('Error', 'API request failed', err);
      const errorMessage = err.response?.data?.message || err.message;
      setError(`Recognition failed: ${errorMessage}`);
      return false;
    }
  };

  const startListening = async () => {
    AudioDebugger.log('Start', 'Starting recording process');
    setIsListening(true);
    setError(null);
    setShowPlaylistOptions(false);
    setStatus('Initializing microphone...');
    
    const audioInitialized = await initializeAudio();
    if (!audioInitialized) {
      AudioDebugger.log('Error', 'Audio initialization failed');
      setIsListening(false);
      return;
    }

    setStatus('Recording...');
    startTime.current = Date.now();
    mediaRecorder.current.start(100); // Collect data every 100ms

    // Update progress
    progressInterval.current = setInterval(() => {
      const elapsed = Date.now() - startTime.current;
      const progress = Math.min(100, (elapsed / RECORD_TIME) * 100);
      setRecordingProgress(progress);
      setStatus(`Recording: ${(elapsed / 1000).toFixed(1)}/${(RECORD_TIME / 1000).toFixed(1)} seconds`);
    }, 100);

    // Stop recording after RECORD_TIME
    setTimeout(() => {
      if (mediaRecorder.current?.state === 'recording') {
        AudioDebugger.log('Recording', 'Maximum time reached, stopping');
        stopListening();
      }
    }, RECORD_TIME);
  };

  const addToPlaylist = (playlistId) => {
    if (recognizedSong) {
      setPlaylists(prev => ({
        ...prev,
        [playlistId]: [
          ...(prev[playlistId] || []),
          recognizedSong
        ]
      }));
      setShowPlaylistOptions(false);
      setRecognizedSong(null);
    }
  };

  return (
    <Box sx={{ maxWidth: 600, mx: 'auto', mt: 4, p: 2 }}>
      <Button
        variant="contained"
        color={isListening ? "secondary" : "primary"}
        fullWidth
        onClick={startListening}
        disabled={isListening}
        sx={{ mb: 3, height: 56 }}
      >
        {isListening ? (
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <CircularProgress size={24} color="inherit" sx={{ mr: 1 }} />
            {status}
          </Box>
        ) : (
          "Start Listening"
        )}
      </Button>

      {isListening && (
        <Box sx={{ mb: 2 }}>
          <LinearProgress 
            variant="determinate" 
            value={recordingProgress} 
            sx={{ 
              height: 10, 
              borderRadius: 5,
              backgroundColor: 'rgba(255,255,255,0.1)',
              '& .MuiLinearProgress-bar': {
                backgroundColor: '#4CAF50'
              }
            }} 
          />
        </Box>
      )}

      {error && (
        <Typography color="error" sx={{ mb: 2 }}>
          {error}
        </Typography>
      )}

      {recognizedSong && showPlaylistOptions && (
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              {recognizedSong.title}
            </Typography>
            <Typography color="text.secondary" gutterBottom>
              by {recognizedSong.artist}
            </Typography>
            <Typography variant="body2" sx={{ mt: 2, mb: 2 }}>
              Add to playlist:
            </Typography>
            <Stack spacing={1}>
              {MOOD_PLAYLISTS.map(playlist => (
                <Button
                  key={playlist.id}
                  variant="contained"
                  onClick={() => addToPlaylist(playlist.id)}
                  sx={{
                    backgroundColor: playlist.color,
                    '&:hover': {
                      backgroundColor: playlist.color,
                      opacity: 0.9
                    }
                  }}
                >
                  {playlist.name}
                </Button>
              ))}
            </Stack>
          </CardContent>
        </Card>
      )}

      {Object.entries(playlists).map(([playlistId, songs]) => (
        songs.length > 0 && (
          <Card key={playlistId} sx={{ mb: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom sx={{ 
                color: MOOD_PLAYLISTS.find(p => p.id === playlistId)?.color 
              }}>
                {MOOD_PLAYLISTS.find(p => p.id === playlistId)?.name}
              </Typography>
              {songs.map((song, index) => (
                <Typography key={index} sx={{ mb: 1 }}>
                  {song.title} - {song.artist}
                </Typography>
              ))}
            </CardContent>
          </Card>
        )
      ))}
    </Box>
  );
};

export default SongRecognition;
