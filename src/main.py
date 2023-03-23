import cv2 as cv
import numpy as np
import pyautogui
import threading
import time
import datetime


def thread_function(video_fps):
    global stop
    stop = False
    while True:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        out.write(frame)
        time.sleep(1000/video_fps/1000)
        if stop:
            break


SCREEN_SIZE = tuple(pyautogui.size())
fourcc = cv.VideoWriter_fourcc(*"XVID")
fps = 15.0

fecha_hora = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
out = cv.VideoWriter(f'{fecha_hora}_output.avi', fourcc, fps, (SCREEN_SIZE))
x = threading.Thread(target=thread_function, args=(fps,), daemon=True)

x.start()
key = input('Presioná una tecla para frenar la grabación... ')
stop = True

if stop:
    cv.destroyAllWindows()
    out.release()
    img = pyautogui.screenshot(region=(0, 0, 300, 400))
    print('Grabación finalizada')
