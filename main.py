from Display_button import DisplayApp
from Record_canvas import TestApp
import concurrent.futures

if __name__ == '__main__':
    func1 = DisplayApp().run()
    func2 = TestApp().run()
    executor = concurrent.futures.ProcessPoolExecutor(max_workers=2)
    executor.submit(func1)
    executor.submit(func2)

