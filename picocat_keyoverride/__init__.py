from PhiLia093.h import *

GAMENAME = 'PICO PARK:Classic Edition'

def onn_space_pressed(e) -> None:
    game = FindWindow(None, GAMENAME)
    if game:
        PostMessage(game, WM_KEYDOWN, ['W', 0x57][1], 0)

def onn_space_released(e) -> None:
    game = FindWindow(None, GAMENAME)
    if game:
        PostMessage(game, WM_KEYUP, ['W', 0x57][1], 0)

keyboard.on_press_key('space', onn_space_pressed)
keyboard.on_release_key('space', onn_space_released)

def _loop():
    while True:
        keyboard.wait('space')

t = threading.Thread(target=_loop, daemon=True)

def start() -> Thread:
    t.start()
    return t