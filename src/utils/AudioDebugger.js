export class AudioDebugger {
  static DEBUG = true;

  static log(context, message, data = null) {
    if (!this.DEBUG) return;
    
    const timestamp = new Date().toISOString().split('T')[1];
    const prefix = `[${timestamp}] [${context}]`;
    
    if (data) {
      console.log(prefix, message, data);
    } else {
      console.log(prefix, message);
    }
  }

  static async analyzeStream(stream) {
    if (!this.DEBUG) return;

    const track = stream.getAudioTracks()[0];
    const settings = track.getSettings();
    const capabilities = track.getCapabilities();
    const constraints = track.getConstraints();

    this.log('AudioTrack', 'Settings:', settings);
    this.log('AudioTrack', 'Capabilities:', capabilities);
    this.log('AudioTrack', 'Constraints:', constraints);

    // Test audio levels
    const audioContext = new AudioContext();
    const source = audioContext.createMediaStreamSource(stream);
    const analyser = audioContext.createAnalyser();
    analyser.fftSize = 256;
    source.connect(analyser);

    const dataArray = new Uint8Array(analyser.frequencyBinCount);
    
    const checkLevel = () => {
      analyser.getByteFrequencyData(dataArray);
      const average = dataArray.reduce((a, b) => a + b) / dataArray.length;
      this.log('AudioLevel', `Current level: ${average.toFixed(2)}`);
    };

    // Check levels for 2 seconds
    for (let i = 0; i < 20; i++) {
      checkLevel();
      await new Promise(resolve => setTimeout(resolve, 100));
    }

    audioContext.close();
  }

  static logAudioData(audioBlob) {
    if (!this.DEBUG) return;

    this.log('AudioData', `Size: ${audioBlob.size} bytes`);
    this.log('AudioData', `Type: ${audioBlob.type}`);
  }
}
