import time
class Sample:

    def __init__(self,text):
        self.text = text

    def testsample(self):
        text_list = []
        text_list = self.text.split()
        for i in text_list:
            time.sleep(1)
            print(i)