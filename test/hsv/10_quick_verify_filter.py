# This file is just for quickly verifying the position of the grab areas in game
# I have made it standalone for simplicity of setup, no filters being used, etc,
import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture
from hsvfilter import grab_object_preset
from vision import Vision

os.chdir(os.path.dirname(os.path.abspath(__file__)))

filter, custom_rect = grab_object_preset(
    object_name="dungeon_check")

wincap = WindowCapture("Rusty Hearts: Revolution - Reborn ", custom_rect)

vision = Vision('dunchk.jpg')

loop_time = time()
while(True):
    # get an updated image of the game
    screenshot = wincap.get_screenshot()
    output_image = vision.apply_hsv_filter(
        screenshot, filter)
    cv.imshow('Viewbox', output_image)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')
