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
                rows:4
                GridLayout:
                    rows:3
                    cols:2
                    size_hint_y: 0.4
                    
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
                Wordlist:
                    id: wordlist    
            Button:
                size_hint_x: 0.5
                id: button1_b
                text: "録音START"
                font_size: 24
                # on_press: root.buttonClicked1_a()
                on_press: root.buttonClicked1_b()
            # GridLayout:
            #     rows:2     
            #     Button:
            #         size_hint_x: 1
            #         id: button1_a
            #         text: "録音START"
            #         font_size: 48
            #         on_press: root.buttonClicked1_a()
            # 
            #     Button:
            #         size_hint_x: 1
            #         id: button1_b
            #         text: "画面START"
            #         font_size: 48
            #         on_press: root.buttonClicked1_b()
            Button:
                size_hint_x: 0.4
                id: button2
                text: "測定"
                font_size: 48
                on_press: root.buttonClicked2() #ボタンをクリックした時にpython側の関数を呼ぶ
        
<Wordlist@GridLayout>: #Dynamic class
    rows: 2
    cols: 2
    Button:
        id: word1_btn
        text: "あ い う え お"
        on_press: app.root.press_word(self)
    Button:
        id: word2_btn
        text: "か き く け こ"
        on_press: app.root.press_word(self)
    Button:
        id: word3_btn
        text: "さ し す せ そ"
        on_press: app.root.press_word(self)
    Button:
        id: word4_btn
        text: "た ち つ て と"
        on_press: app.root.press_word(self)
      
""")
# def display(disp_word,num):
#     global display_word1
#     word = "休止"
#     if not num % 5 == 0:
#         word_list = disp_word.split()
#         try:
#             ans = num//5
#             word = str(word_list[ans])
#         except:
#             word = "何もありません"
#     display_word1 = word


class MyCanvas(FloatLayout):
    global display_word1
    text = StringProperty()  # プロパティの追加
    name = ObjectProperty(None)
    year = ObjectProperty(None)
    month = ObjectProperty(None)
    day = ObjectProperty(None)
    voice_word = ObjectProperty(None)
    c_display = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MyCanvas, self).__init__(**kwargs)
        display_word1 = "STARTで録音開始"
        self.text = display_word1


    def buttonClicked_thread(self):
        s = Sample(self.voice_word.text)
        # c1 = Clock.schedule_once(partial(self.my_callback, 1), 1)
        # c2 = Clock.schedule_once(partial(self.my_callback, 2), 2)
        # executor = ThreadPoolExecutor(max_workers=4)
        # # executor.submit(self.buttonClicked_a2())
        # executor.submit(c1)
        # executor.submit(c2)
        # executor.submit(s.testsample())
        # executor.submit(self.buttonClicked_a1())
        # loop = asyncio.get_event_loop()
        # gather = asyncio.gather(
        #     self.buttonClicked_a2(),
        #     self.buttonClicked_a1(),
        # )
        # loop.run_until_complete(gather)

        loop = asyncio.get_event_loop()
        gather = asyncio.gather(
            self.buttonClicked1_b(),
            self.buttonClicked1_a(),
            #s.testsample()
        )
        loop.run_until_complete(gather)

    def buttonClicked1_a(self):        # ボタンをクリック時
        name = self.name.text
        date = f"{self.year.text}{self.month.text}{self.day.text}"
        word = self.voice_word.text
        print(f"name is {self.name.text}")
        print(f"date is {date}")
        max_time = 25
        ma = myaudio(name, date, word)
        ma.pyrecord()

    def buttonClicked1_b(self):
        word_list = self.voice_word.text.split()
        num = 2
        for w in word_list:
            Clock.schedule_once(partial(self.my_callback, w), num)
            num += 2
        Clock.schedule_once(partial(self.my_callback, "あ"), 12)

    def buttonClicked2(self):        # ボタンをクリック時
        subprocess.Popen(r"C:\Users\yokoo takaya\Desktop\WS151\WS.EXE")

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