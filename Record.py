import pyaudio
import wave
import time

class myaudio:

    def __init__(self,name,date,word):
        self.name = name
        self.date = date
        self.word = word

    def pyrecord(self):
        a = pyaudio.PyAudio()

        hostAPICount = a.get_host_api_count()
        print("Host API Count = " + str(hostAPICount))

        for cnt in range(hostAPICount):
            print(a.get_host_api_info_by_index(cnt))

        DEVICE_INDEX = 0
        CHUNK = 1024 #音源から1回読み込むときのデータサイズ。1024(=2の10乗) とする場合が多い
        FORMAT = pyaudio.paInt16 # 16bit
        CHANNELS = 1             # monaural
        RATE = 48000             # sampling frequency [Hz]

        time = 10 # record time [s] 5sなら0-4sデータ
        output_path = f"./{self.name}_{self.date}_{self.word}.wav"
        print(f"output_path is {output_path}")
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        input_device_index = DEVICE_INDEX,
                        frames_per_buffer=CHUNK)

        print("recording ...")

        frames = []

        for i in range(0, int(RATE / CHUNK * time)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("done.")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(output_path, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()