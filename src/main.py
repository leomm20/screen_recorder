import cv2 as cv
import numpy as np
import pyautogui
import threading
import time
import datetime
from pynput import mouse
from avi2mp4 import convert_avi2mp4


def on_click(x, y, button, pressed):
    global mouse_x, mouse_y
    if pressed:
        mouse_x = x
        mouse_y = y
    else:
        mouse_x = 0
        mouse_y = 0


def thread_function(video_fps):
    global stop, out, mouse_x, mouse_y, imprime_mouse
    stop = False
    while True:
        img_screen = pyautogui.screenshot()
        x, y = pyautogui.position()
        frame = np.array(img_screen)
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        if imprime_mouse:
            if mouse_x == 0:
                frame = cv.circle(frame, (x, y), 10, (0, 0, 255), -1)
            else:
                frame = cv.circle(frame, (x, y), 30, (0, 0, 255), -1)
        out.write(frame)
        time.sleep(1000/video_fps/1000)
        if stop:
            time.sleep(2)
            break


# MODIFICAR SI ES NECESARIO:
fps = 15.0
imprime_mouse = True
# FIN MODIFICAR


SCREEN_SIZE = tuple(pyautogui.size())
fourcc = cv.VideoWriter_fourcc(*"XVID")
fecha_hora = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
filename = f'{fecha_hora}_output.avi'
out = cv.VideoWriter(filename, fourcc, fps, SCREEN_SIZE)
thread = threading.Thread(target=thread_function, args=(fps,), daemon=True)

mouse_x = 0
mouse_y = 0
mouse_listener = mouse.Listener(
    on_click=on_click)
mouse_listener.start()

thread.start()
key = input('Presioná Enter para frenar la grabación... ')
stop = True

if stop:
    print('Guardando archivo...')
    time.sleep(1)
    out.release()
    time.sleep(1)
    cv.destroyAllWindows()
    img = pyautogui.screenshot(region=(0, 0, 300, 400))
    new_filename = convert_avi2mp4(filename)
    print('Grabación finalizada')
