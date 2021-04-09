import cv2 as cv
import numpy as np
import os
from time import time, sleep
import pydirectinput
from pynput.keyboard import Key, Listener, KeyCode, Controller
import threading


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

# Attempt 1
# while True:
#     sleep(0.5)
#     if cv.waitKey(1) == ord('q'):
#         break
#     if cv.waitKey(1) == ord('e'):
#         basic_combo()

# Attempt 2, fixing problem of not having a window
# def on_press(key):
#     pass
#     # print('{0} pressed'.format(
#     #     key))


# def on_release(key):
#     # print('{0} release'.format(
#     #     key))
#     if key == KeyCode(char='e'):
#         basic_combo()
#     if key == Key.esc:
#         # Stop listener
#         return False


# def start():
#     # Collect events until released
#     with Listener(
#             on_press=on_press,
#             on_release=on_release) as listener:
#         listener.join()

#     print("Got to here")
# start()

# Attempt 3, fixing problem of not being threaded
listener = None
keyPressed = None
running = True


def on_press(key):
    if key == Key.esc:
        # Stop listener
        global running
        running = False
        return False


def on_release(key):
    global keyPressed
    keyPressed = key.char


def CheckWhichKeyIsPressed():
    global listener

    if listener == None:
        listener = Listener(on_press=on_press,
                            on_release=on_release, suppress=True)
        listener.start()
    print("Got to here")


CheckWhichKeyIsPressed()
while running:
    sleep(0.1)
