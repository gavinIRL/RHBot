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
#custom_rect = list(map(lambda x: int(x*1.5), custom_rect))
#wincap = WindowCapture(custom_rect=custom_rect)

# Grab the gamename from the text file
with open("gamename.txt") as f:
    gamename = f.readline()

wincap = WindowCapture(gamename, custom_rect)
# target = 'dunchk.jpg'
# target_img = cv.imread(target, cv.IMREAD_UNCHANGED)
# target_filtered =
vision = Vision('dunchk_67filt.jpg')

loop_time = time()
while(True):
    # get an updated image of the game
    screenshot = wincap.get_screenshot()
    output_image = vision.apply_hsv_filter(
        screenshot, filter)
    dunchk_rectangles = vision.find(
        output_image, threshold=0.31, epsilon=0.4)
    output_image_rect = vision.draw_rectangles(screenshot, dunchk_rectangles)
    cv.imshow('Filtered', output_image)
    cv.imshow('Box', output_image_rect)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')
