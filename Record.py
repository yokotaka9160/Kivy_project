import pyaudio
import wave
import os

class myaudio:

    def __init__(self,name,date,word,recotime):
        self.name = name
        self.date = date
        self.word = word
        self.recotime = recotime

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

        time = self.recotime # record time [s] 5sなら0-4sデータ
        new_path = f"audio_data/{self.name}"
        os.makedirs(new_path,exist_ok=True)

        output_path = f"{new_path}/{self.name}_{self.date}_{self.word}.wav"
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

        num = 1
        is_file = os.path.isfile(output_path)
        while is_file:
            output_path = f"{output_path}_ver{num}"
            is_file = os.path.isfile(output_path)
            num += 1

        wf = wave.open(output_path, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()