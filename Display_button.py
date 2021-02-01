from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from functools import partial
from kivy.uix.button import Button
import japanize_kivy
import pandas as pd

Builder.load_string('''
<Btn_Canvas>
    voice_word: voice_word
    c_display: c_display
    word_buttons: word_buttons
    
    BoxLayout:
        orientation: 'vertical' # 'horizontal'だと列分割 verticalは行分割
        
        Label:
            size_hint_y: 0.5
            id: c_display
            text: root.text
            font_size: 60
        Label:
            size_hint_y: 0.1
            id: voice_word
            text: "発音言語"
        StackLayout:
            size_hint_y: 0.25
            id: word_buttons
            orientation: 'lr-tb'
            # size_hint: 1, .1
        
        Button:
            size_hint_y: 0.15
            id: button1_a
            text: "Display START"
            font_size: 36
            on_press: root.buttonClicked()

# <Wordlist@BoxLayout>: #Dynamic class
#     size_hint_y: 0.1
#     orientation: 'horizontal'
#     Button:
#         id: word1_btn
#         text: "あ い う え お"
#         on_press: app.root.press_word(self)
#     Button:
#         id: word2_btn
#         text: "か き く け こ"
#         on_press: app.root.press_word(self)
#     Button:
#         id: word3_btn
#         text: "さ し す せ そ"
#         on_press: app.root.press_word(self)
#     Button:
#         id: word4_btn
#         text: "た ち つ て と"
#         on_press: app.root.press_word(self)
''')
class Btn_Canvas(FloatLayout):
    global display_word2
    text = StringProperty()
    word_buttons = ObjectProperty()
    c_display = ObjectProperty(None)
    voice_word = ObjectProperty(None)


    def __init__(self, **kwargs):
        super(Btn_Canvas, self).__init__(**kwargs)
        display_word2 = "休止"
        self.text = display_word2
        self.word_type = "3" #発音音声タイプを入力してください　1:モーラ　2:音声記号表 3:ATR503
        self.panda = False

        if self.word_type == "1":
            self.word_dict = {"モーラ（あ）": "あ い う え お や ゆ よ", "モーラ（か）": "か き く け こ きゃ きゅ きょ",
                              "モーラ（が）": "が ぎ ぐ げ ご ぎゃ ぎゅ ぎょ",
                              "モーラ（さ）": "さ し す せ そ しゃ しゅ しょ","モーラ（ざ）": "ざ じ ず ぜ ぞ じゃ じゅ じょ",
                              "モーラ（た）": "た ち つ て と ちゃ ちゅ ちょ", "モーラ（だ）": "だ で ど",
                              "モーラ（な）": "な に ぬ ね の にゃ にゅ にょ ", "モーラ（は）": "は ひ ふ へ ほ ひゃ ひゅ ひょ ",
                              "モーラ（ぱ）": "ぱ ぴ ぷ ぺ ぽ ぴゃ ぴゅ ぴょ",
                              "モーラ（ま）": "ま み む め も みゃ みゅ みょ", "モーラ（ら）": "ら り る れ ろ りゃ りゅ りょ", "モーラ（わ）": "わ"}
        elif self.word_type == "2":
            self.word_dict = {"音記（あ）": "あ い う え お ", "音記（か）": "か き く け こ きゃ きゅ きょ",
                              "音記（さ）": "さ し す せ そ しゃ しゅ しょ","音記（た）": "た ち つ て と ちゃ ちゅ ちょ",
                              "音記（な）": "な に ぬ ね の にゃ にゅ にょ ","音記（は）": "は ひ ふ へ ほ ひゃ ひゅ ひょ ",
                              "音記（ま）": "ま み む め も みゃ みゅ みょ","音記（や）": "や　ゆ　よ","音記（ら）": "ら り る れ ろ りゃ りゅ りょ",
                              "音記（わ）": "わ","音記（が）": "が ぎ ぐ げ ご ぎゃ ぎゅ ぎょ","音記（ざ）": "ざ じ ず ぜ ぞ じゃ じゅ じょ",
                              "音記（だ）": "だ で ど","音記（ば）": "ば び ぶ べ ぼ びゃ びゅ びょ","音記（ぱ）": "ぱ　ぴ　ぷ　ぺ　ぽ　ぴゃ　ぴゅ　ぴょ",
                               }
        elif self.word_type == "3":
            df_ATR = pd.read_excel()
            ATR_list = df_ATR["発話文"].values.tolist()
            ATR_keys, ATR_values, ATR_keys2, ATR_values2 = [], [], [], []
            for ATR_word in ATR_list:
                if 'a' in ATR_word.split(":")[0]:
                    ATR_keys.append(ATR_word.split(":")[0])
                    ATR_values.append(ATR_word.split(":")[1])
            ATR_num = len(ATR_keys) // 5
            for i in range(ATR_num):
                ATR_keys2.append(f"ATR_a{i * 5 + 1}_{i * 5 + 5}")
                ATR_values2.append(
                    f"{ATR_values[i * 5]}/{ATR_values[i * 5 + 1]}/{ATR_values[i * 5 + 2]}/"
                    f"{ATR_values[i * 5 + 3]}/{ATR_values[i * 5 + 4]}")
            ATR_dict = dict(zip(ATR_keys2, ATR_values2))
            self.word_dict = ATR_dict
            self.c_display.font_size = 36

        word_list = list(self.word_dict.keys())
        for v_word in word_list:
            button = Button(text=v_word, size_hint=(.2, .25))
            button.bind(on_press=self.press_word)
            self.word_buttons.add_widget(button)

    def press_word(self,value):
        word = value.text
        print(self.word_dict[word])
        print(type(self.word_dict[word]))
        self.voice_word.text = self.word_dict[word]

    def buttonClicked(self):
        word2 = self.voice_word.text
        v_start = 4
        if self.word_type == "3":
            w_list = word2.split("/")
            dtime = 6
        else:
            w_list = word2.split()
            dtime = 2

        for k in range(5):
            start_word = f"開始まで{4-k}"
            Clock.schedule_once(partial(self.my_callback, start_word), k)

        for i,j in enumerate(w_list):
            p_start = v_start + dtime
            if self.word_type != "3":
                vword = f"{j}ー"
            else:
                vword = f"{j}"
            print(v_start)
            print(p_start)
            Clock.schedule_once(partial(self.my_callback, vword),v_start)
            if self.panda == True:
                Clock.schedule_once(partial(self.my_callback, "ぱんだ"),p_start)
            else:
                Clock.schedule_once(partial(self.my_callback, ""), p_start)
            v_start = p_start + 2

    def my_callback(self,num,dt):
        print("起動")
        display_word2 = f"{num}"
        print(f"display_word2 is {display_word2}")
        self.text = display_word2

class DisplayApp(App):
    def __init__(self, **kwargs):
        super(DisplayApp, self).__init__(**kwargs)
        self.title = 'Display Window'  # ウィンドウの名前を変更

    def build(self):
        return Btn_Canvas()

if __name__ == '__main__':
    DisplayApp().run()