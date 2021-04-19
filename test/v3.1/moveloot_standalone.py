# This will be the upgraded v2 move and loot only file
# But with quick restart capability and modular design
# No longer meant to be used as main file

import cv2 as cv
import os
from time import time, sleep
import numpy as np
from pynput.keyboard import Key, Listener, KeyCode
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import grab_object_preset
from actionsv2 import Movement_Handler, Actions


class StandaloneMoveLoot():
    def __init__(self, controller) -> None:
        pass
