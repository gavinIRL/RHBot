import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import HsvFilter, grab_object_preset

# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("gamename.txt") as f:
    gamename = f.readline()

filter, custom_rect = grab_object_preset("enemy_map_loc")
WindowCapture.list_window_names()
# initialize the WindowCapture class
wincap = WindowCapture(gamename)

# initialize the Vision class
vision_limestone = Vision('player_nodir2.jpg')
# initialize the trackbar window
vision_limestone.init_control_gui()

loop_time = time()
while(True):

    # get an updated image of the game
    screenshot = wincap.get_screenshot()
    # pre-process the image
    output_image = vision_limestone.apply_hsv_filter(screenshot)
    # display the processed image
    cv.imshow('Matches', output_image)

    # debug the loop rate
    # print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')
