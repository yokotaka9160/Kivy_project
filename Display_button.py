from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from functools import partial

Builder.load_string('''
<Btn_Canvas>
    
    c_display: c_display
    BoxLayout:
        orientation: 'vertical' # 'horizontal'だと列分割 verticalは行分割
        
        Label:
            id: c_display
            text: root.text
            font_size: 96
        Button:
            id: button1_a
            text: "Display START"
            font_size: 48
            on_press: root.buttonClicked()
''')
class Btn_Canvas(FloatLayout):
    global display_word2
    text = StringProperty()
    c_display = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Btn_Canvas, self).__init__(**kwargs)
        display_word2 = "休止"
        self.text = display_word2

    def buttonClicked(self):
        Clock.schedule_once(partial(self.my_callback, 1), 1)
        Clock.schedule_once(partial(self.my_callback, 2), 2)
        Clock.schedule_once(partial(self.my_callback, 3), 3)
        Clock.schedule_once(partial(self.my_callback, 4), 4)

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