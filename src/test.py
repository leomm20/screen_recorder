from pynput import mouse


def on_scroll(x=0, y=0, dx=0, dy=0):
    global mouse_scroll
    if dx == 0 and dy > 0:
        mouse_scroll = 'arriba'
    elif dx == 0 and dy < 0:
        mouse_scroll = 'abajo'
    elif dx < 0:
        mouse_scroll = 'izquierda'
    elif dx > 0 and dy == 0:
        mouse_scroll = 'derecha'
    else:
        mouse_scroll = ''


mouse_scroll = ''

mouse_listener = mouse.Listener(
    on_scroll=on_scroll)
mouse_listener.start()

while True:
    print(mouse_scroll)
