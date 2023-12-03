import pyaudio
import wave

def record_audio(output_filename="output.wav", record_seconds=3):
    # Basic parameter setup
    CHUNK = 1024  # Number of frames per buffer
    FORMAT = pyaudio.paInt16  # Sample size and format
    CHANNELS = 1  # Number of audio channels
    RATE = 16000  # Sample rate set to 16kHz

    p = pyaudio.PyAudio()

    # Start recording
    print("Recording started...")
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    for _ in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording ended")

    # Stop recording
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save as a WAV file
    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"Audio has been saved as {output_filename}")

if __name__ == "__main__":
    record_audio("mine.wav", 10)
