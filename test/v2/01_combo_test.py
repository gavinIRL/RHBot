import cv2 as cv
import numpy as np
import os
from time import time, sleep
import pydirectinput
from pynput.keyboard import Key, Listener, KeyCode


def basic_combo():
    print("Basic combo starting")
    pydirectinput.keyDown("d")
    sleep(0.1)
    pydirectinput.keyUp("d")
    sleep(0.1)
    pydirectinput.keyDown("x")
    sleep(0.1)
    pydirectinput.keyUp("x")
    sleep(0.1)
    pydirectinput.keyDown("x")
    sleep(0.1)
    pydirectinput.keyUp("x")


# while True:
#     sleep(0.5)
#     if cv.waitKey(1) == ord('q'):
#         break
#     if cv.waitKey(1) == ord('e'):
#         basic_combo()

def on_press(key):
    pass
    # print('{0} pressed'.format(
    #     key))


def on_release(key):
    # print('{0} release'.format(
    #     key))
    if key == KeyCode(char='e'):
        basic_combo()
    if key == Key.esc:
        # Stop listener
        return False


# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
