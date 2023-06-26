import os
import sys
import cv2 as cv
import numpy as np
import pyautogui
import threading
import time
import datetime
import pydub
import soundfile as sf
from pynput import mouse
"""
en windows, modificar, en mouse y en keyboard \__init__.py:
# from pynput._util import backend, Events
from pynput._util import Events
from pynput.keyboard import _win32 as backend
# backend = backend(__name__)
KeyCode = backend.KeyCode
"""
from avi2mp4 import convert_avi2mp4
from moviepy.editor import VideoFileClip, AudioFileClip


def merge_audio_video(video_file, audio_file, output_file):
    video = VideoFileClip(video_file)
    audio = AudioFileClip(audio_file)

    video = video.set_audio(audio)
    video.write_videofile(output_file, codec='libx264', audio_codec='aac')


def on_click(x, y, button, pressed):
    global mouse_x, mouse_y
    if pressed:
        mouse_x = x
        mouse_y = y
    else:
        mouse_x = 0
        mouse_y = 0


def thread_function(video_fps, filename_):
    global stop, mouse_x, mouse_y, imprime_mouse, stopped_video, video, fecha_hora
    SCREEN_SIZE = tuple(pyautogui.size())
    fourcc = cv.VideoWriter_fourcc(*"XVID")
    out = cv.VideoWriter(filename_, fourcc, fps, SCREEN_SIZE)
    stop = False
    while True:
        start_time = time.time()
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
        elapsed_time = time.time() - start_time
        sleep_time = max(0, 1.0 / video_fps - elapsed_time)
        time.sleep(sleep_time)
        # time.sleep(1000/video_fps/1000)
        if stop:
            time.sleep(2)
            break
    print('Guardando archivo de video...')
    time.sleep(1)
    out.release()
    time.sleep(1)
    cv.destroyAllWindows()
    # img = pyautogui.screenshot(region=(0, 0, 300, 400))
    time.sleep(3)
    video = convert_avi2mp4(filename_)
    time.sleep(1)
    os.remove(filename_)
    stopped_video = True


def adjust_audio_duration(file_path, target_duration_seconds):
    print(target_duration_seconds)
    audio, sample_rate = sf.read(file_path)
    target_duration_samples = int(target_duration_seconds * sample_rate)
    adjusted_audio = audio[:target_duration_samples]
    sf.write(file_path[:-4] + '_.wav', adjusted_audio, sample_rate)
    return file_path[:-4] + '_.wav'


def grabar_audio():
    print('Grabando audio!\n')
    global stop, stopped_audio, filename, audio

    import sounddevice as sd
    from scipy.io.wavfile import write

    fs = 44100  # Sample rate
    seconds = 3600  # Duration of recording

    inicio = datetime.datetime.now()
    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    while not stop:
        time.sleep(2)
    fin = datetime.datetime.now()
    duracion = fin - inicio
    duracion = duracion.seconds
    sd.stop()

    time.sleep(2)
    archivo = filename[:-4] + '.wav'
    write(archivo, fs, myrecording)  # Save as WAV file
    time.sleep(2)
    print('audio grabado')
    audio = adjust_audio_duration(archivo, duracion)
    print('optimizando audio')
    time.sleep(2)
    seg = pydub.AudioSegment.from_wav(audio)
    # silencio = pydub.AudioSegment.silent(500)
    # seg = silencio + seg
    seg.export(audio)
    time.sleep(2)
    os.remove(archivo)
    stopped_audio = True


# MODIFICAR SI ES NECESARIO:
fps = 15.0
imprime_mouse = True
# FIN MODIFICAR

stop = False
stopped_video = False
stopped_audio = False

con_audio = input('Con audio? (s/n/[e para salir]): ')
while con_audio not in ('s', 'n', 'S', 'N', 'e', 'E'):
    con_audio = input('Con audio? (s/n/[e para salir]): ')
if con_audio.lower() == 'e':
    print('Bye!')
    sys.exit()
elif con_audio.lower() == 's':
    con_audio = True
else:
    con_audio = False

fecha_hora = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')
filename = f'{fecha_hora}_output.avi'

mouse_x = 0
mouse_y = 0
mouse_listener = mouse.Listener(
    on_click=on_click)
mouse_listener.start()

thread = threading.Thread(target=thread_function, args=(fps, filename,), daemon=True)
thread_audio = threading.Thread(target=grabar_audio, daemon=True)

video = ''
audio = ''
final = filename[:-4] + '_.mp4'

thread.start()
if con_audio:
    thread_audio.start()
key = input('Presioná Enter 2 veces para frenar la grabación...')
print('Comenzando armado de archivo mp4')
stop = True

while not stopped_video:
    time.sleep(1)
    print('.')
print('Grabación de video finalizada')
if con_audio:
    while not stopped_audio:
        time.sleep(1)
    print('Grabación de audio finalizada')
merge_audio_video(video, audio, final)
os.remove(video)
os.remove(audio)
print('\nPROCESO FINALIZADO!!')
os.system(final)
