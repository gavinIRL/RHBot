import cv2 as cv
import numpy as np
import os
from time import time, sleep
import pydirectinput


def basic_combo():
    pydirectinput.keyDown("d")
    sleep(0.1)
    pydirectinput.keyUp("d")
    sleep(0.2)
    pydirectinput.keyDown("x")
    sleep(0.1)
    pydirectinput.keyUp("x")
    sleep(0.2)
    pydirectinput.keyDown("x")
    sleep(0.1)
    pydirectinput.keyUp("x")


while True:
    sleep(0.5)
    if cv.waitKey(1) == ord('q'):
        break
    if cv.waitKey(1) == ord('e'):
        basic_combo()
