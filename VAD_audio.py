from inaSpeechSegmenter import Segmenter
from inaSpeechSegmenter import seg2csv
from pydub import AudioSegment

# 入力のwavファイルのパスを指定
input_file = 
filename = input_file.split()
# 出力のwavファイルのフォルダとプレフィックスまで指定
# → ./output/segment0.wav, ./output/segment1.wav, のような出力を想定
output_file = './output/segment'

# 'smn' は入力信号を音声区間(speeech)、音楽区間(music)、
# ノイズ区間(noise)にラベル付けしてくれる
# detect_genderをTrueにすると、音声区間は男性(male) / 女性(female)のラベルに
# 細分化される
seg = Segmenter(vad_engine='smn', detect_gender=False)

# 区間検出実行（たったこれだけでOK）
segmentation = seg(input_file)

# ('区間ラベル',  区間開始時刻（秒）,  区間終了時刻（秒）)というタプルが
# リスト化されているのが変数 segmentation
# print(segmentation)

# inaSpeechSegmenter単体では分割されたwavを作成してくれないので、
# pydubのAudioSegmentにお世話になる (ありがたいライブラリ)
speech_segment_index = 0
for segment in segmentation:
    # segmentはタプル
    # タプルの第1要素が区間のラベル
    segment_label = segment[0]

    if (segment_label == 'speech'):  # 音声区間

        # 区間の開始時刻の単位を秒からミリ秒に変換
        start_time = segment[1] * 1000
        end_time = segment[2] * 1000

        # 分割結果をwavに出力
        newAudio = AudioSegment.from_wav(input_file)
        newAudio = newAudio[start_time:end_time]
        output_file = output_file + str(speech_segment_index) + '.wav'
        newAudio.export(output_file, format="wav")

        speech_segment_index += 1
        del newAudio
seg2csv(segmentation, f"./segment/myseg_{}.csv")