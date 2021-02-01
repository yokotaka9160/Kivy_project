from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.clock import Clock
import japanize_kivy
from kivy.uix.textinput import TextInput
import subprocess
from Record import myaudio
from Sample import Sample
import threading
import concurrent.futures
from functools import partial
from multiprocessing import Process
import asyncio
from concurrent.futures import ThreadPoolExecutor
from kivy.uix.button import Button

#size_hint_y : y座標(0~2)
# rgba : r(赤色),g（黄色）,b（青色）,a（透明度）
#self.pos : Labelのxy座標
#self.size : Labelの幅と高さの値
#予約語 : self ・・・ そのWidgetを取得
#        root ・・・ rootWidgetを取得
#        app ・・・ Appを取得
Builder.load_string("""
<MyCanvas>
    name: name
    year: year
    month: month
    day: day
    voice_word: voice_word
    c_display: c_display
    word_buttons: word_buttons
    
    BoxLayout:
        orientation: 'vertical' # 'horizontal'だと列分割 verticalは行分割
        
        Label:
            id: c_display
            text: root.text
            font_size: 96
            size_hint_y: 1 
            
        BoxLayout:
            orientation: 'horizontal'

            GridLayout:
                rows:3
                GridLayout:
                    rows:3
                    cols:2
                    size_hint_y: 0.3
                    
                    Label:
                        text: "名前(ローマ字入力)"
                    TextInput:
                        id: name
                        text: ''
                    Label:
                        text: "年"
                    Spinner:    # 年のリスト表示
                        id: year
                        size_hint: .1,1
                        halign: 'center'
                        valign: 'middle'
                        text_size: self.size
                        text:'2020'
                        values: [str(y) for y in range(2020, 2022) ]
                    BoxLayout:
                        orientation: 'horizontal'
                        Label:
                            text: "月"
                        Spinner:
                            id: month   # 月のリスト表示
                            text:'01'
                            values: ['{0:02d}'.format(x)  for x in range(1,13)]
                    BoxLayout:
                        orientation: 'horizontal'
                        Label:
                            text: "日"
                        Spinner:    # 日のリスト表示
                            id: day
                            text:'01'
                            values: ['{0:02d}'.format(x)  for x in range(1,30)] 
                Label:
                    size_hint_y: 0.2
                    id: voice_word
                    text: "発音言語"
                StackLayout:
                    size_hint_y: 0.5
                    id: word_buttons
                    orientation: 'lr-tb'

            Button:
                size_hint_x: 0.5
                id: button1_b
                text: "録音START"
                font_size: 24
                on_press: root.buttonClicked1_a()
                # on_press: root.buttonClicked1_b()

            Button:
                size_hint_x: 0.4
                id: button2
                text: "測定"
                font_size: 48
                on_press: root.buttonClicked2() #ボタンをクリックした時にpython側の関数を呼ぶ
        
""")


class MyCanvas(FloatLayout):
    global display_word1
    text = StringProperty()  # プロパティの追加
    name = ObjectProperty(None)
    year = ObjectProperty(None)
    month = ObjectProperty(None)
    day = ObjectProperty(None)
    voice_word = ObjectProperty(None)
    c_display = ObjectProperty(None)
    word_buttons = ObjectProperty()

    def __init__(self, **kwargs):
        super(MyCanvas, self).__init__(**kwargs)
        display_word1 = "STARTで録音開始"
        self.text = display_word1
        word_type = "2"  # 発音音声タイプを入力してください　1:モーラ　2:音声記号表
        self.panda = False
        if word_type == "1":
            self.word_dict = {"モーラ（あ）": "あ い う え お や ゆ よ", "モーラ（か）": "か き く け こ きゃ きゅ きょ",
                              "モーラ（が）": "が ぎ ぐ げ ご ぎゃ ぎゅ ぎょ",
                              "モーラ（さ）": "さ し す せ そ しゃ しゅ しょ", "モーラ（ざ）": "ざ じ ず ぜ ぞ じゃ じゅ じょ",
                              "モーラ（た）": "た ち つ て と ちゃ ちゅ ちょ", "モーラ（だ）": "だ で ど",
                              "モーラ（な）": "な に ぬ ね の にゃ にゅ にょ ", "モーラ（は）": "は ひ ふ へ ほ ひゃ ひゅ ひょ ",
                              "モーラ（ぱ）": "ぱ ぴ ぷ ぺ ぽ ぴゃ ぴゅ ぴょ",
                              "モーラ（ま）": "ま み む め も みゃ みゅ みょ", "モーラ（ら）": "ら り る れ ろ りゃ りゅ りょ", "モーラ（わ）": "わ"}
        elif word_type == "2":
            self.word_dict = {"音記（あ）": "あ い う え お ", "音記（か）": "か き く け こ きゃ きゅ きょ",
                              "音記（さ）": "さ し す せ そ しゃ しゅ しょ", "音記（た）": "た ち つ て と ちゃ ちゅ ちょ",
                              "音記（な）": "な に ぬ ね の にゃ にゅ にょ ", "音記（は）": "は ひ ふ へ ほ ひゃ ひゅ ひょ ",
                              "音記（ま）": "ま み む め も みゃ みゅ みょ", "音記（や）": "や　ゆ　よ", "音記（ら）": "ら り る れ ろ りゃ りゅ りょ",
                              "音記（わ）": "わ", "音記（が）": "が ぎ ぐ げ ご ぎゃ ぎゅ ぎょ", "音記（ざ）": "ざ じ ず ぜ ぞ じゃ じゅ じょ",
                              "音記（だ）": "だ で ど", "音記（ば）": "ば び ぶ べ ぼ びゃ びゅ びょ", "音記（ぱ）": "ぱ　ぴ　ぷ　ぺ　ぽ　ぴゃ　ぴゅ　ぴょ",
                              }
        word_list = list(self.word_dict.keys())
        for v_word in word_list:
            button = Button(text=v_word, size_hint=(.2, .35))
            button.bind(on_press=self.press_word)
            self.word_buttons.add_widget(button)

    def buttonClicked1_a(self):        # ボタンをクリック時
        name = self.name.text
        date = f"{self.year.text}{self.month.text}{self.day.text}"
        word = self.voice_word.text
        if self.panda == True:
            send_word = f"{self.voice_word.text}(文字あり)"
        else:
            send_word = f"{self.voice_word.text}(文字なし)"

        print(f"name is {self.name.text}")
        print(f"date is {date}")
        print(len(list(self.word_dict[word])))
        if len(list(self.word_dict[word])) == 5:
            recotime = 25
        elif len(list(self.word_dict[word])) == 1:
            recotime = 15
        else:
            recotime = 45
        ma = myaudio(name, date, send_word, recotime)
        ma.pyrecord()

    def buttonClicked1_b(self):
        word_list = self.voice_word.text.split()
        num = 2
        for w in word_list:
            Clock.schedule_once(partial(self.my_callback, w), num)
            num += 2
        Clock.schedule_once(partial(self.my_callback, "あ"), 12)

    def buttonClicked2(self):        # ボタンをクリック時
        subprocess.Popen(r".\WS151\WS.EXE")

    def press_word(self,value):
        word = value.text
        self.voice_word.text = word

    def my_callback(self,num,dt):
        global display_word1
        print("起動")
        display_word1 = f"{num}"
        print(f"display_word1 is {display_word1}")
        self.text = display_word1

class TestApp(App):
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        self.title = 'Record Support'  # ウィンドウの名前を変更

    def build(self):
        return MyCanvas()

if __name__ == '__main__':
    TestApp().run()