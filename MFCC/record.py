import pyaudio
import wave

def record_audio(output_filename="output.wav", record_seconds=3):
    # 基本参数设置
    CHUNK = 1024  # 每个缓冲区的帧数
    FORMAT = pyaudio.paInt16  # 每个采样的大小和格式
    CHANNELS = 2  # 声道数
    RATE = 44100  # 采样率

    p = pyaudio.PyAudio()

    # 开始录音
    print("开始录音...")
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    for _ in range(0, int(RATE / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("录音结束")

    # 停止录音
    stream.stop_stream()
    stream.close()
    p.terminate()

    # 保存为WAV文件
    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"音频已保存为 {output_filename}")

if __name__ == "__main__":
    record_audio()

