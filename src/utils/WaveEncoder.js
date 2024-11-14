// WAV file format encoder based on WhatAmIHearing's approach
export class WaveEncoder {
  constructor(sampleRate = 44100, bitsPerSample = 16, channels = 1) {
    this.sampleRate = sampleRate;
    this.bitsPerSample = bitsPerSample;
    this.channels = channels;
    this.bytesPerSample = bitsPerSample / 8;
    this.blockAlign = this.bytesPerSample * channels;
    this.byteRate = this.sampleRate * this.blockAlign;
    this.chunks = [];
    this.size = 0;
  }

  writeString(view, offset, string) {
    for (let i = 0; i < string.length; i++) {
      view.setUint8(offset + i, string.charCodeAt(i));
    }
  }

  writeHeader(view, totalSize) {
    // RIFF chunk descriptor
    this.writeString(view, 0, 'RIFF');
    view.setUint32(4, totalSize - 8, true);
    this.writeString(view, 8, 'WAVE');

    // fmt sub-chunk
    this.writeString(view, 12, 'fmt ');
    view.setUint32(16, 16, true); // fmt chunk size
    view.setUint16(20, 1, true); // audio format (PCM)
    view.setUint16(22, this.channels, true);
    view.setUint32(24, this.sampleRate, true);
    view.setUint32(28, this.byteRate, true);
    view.setUint16(32, this.blockAlign, true);
    view.setUint16(34, this.bitsPerSample, true);

    // data sub-chunk
    this.writeString(view, 36, 'data');
    view.setUint32(40, totalSize - 44, true);
  }

  async appendAudioData(audioData) {
    const buffer = await audioData.arrayBuffer();
    this.chunks.push(new Uint8Array(buffer));
    this.size += buffer.byteLength;
  }

  finalize() {
    const headerSize = 44;
    const wavBuffer = new ArrayBuffer(headerSize + this.size);
    const view = new DataView(wavBuffer);
    
    // Write WAV header
    this.writeHeader(view, headerSize + this.size);
    
    // Write audio data
    let offset = headerSize;
    for (const chunk of this.chunks) {
      const uint8View = new Uint8Array(wavBuffer, offset, chunk.length);
      uint8View.set(chunk);
      offset += chunk.length;
    }
    
    return new Blob([wavBuffer], { type: 'audio/wav' });
  }
}
