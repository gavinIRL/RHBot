# This file is for testing difference between one big screenshot
# Or multiple individual smaller onces
# In terms of frame rate
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

filter, custom_rect = grab_object_preset("loot_far")
WindowCapture.list_window_names()
# initialize the WindowCapture class
# wincap = WindowCapture("Rusty Hearts: Revolution - Reborn ")
wincap2 = WindowCapture("Rusty Hearts: Revolution - Reborn ", custom_rect)

# initialize the Vision class
vision_limestone = Vision('dunchk_67.jpg')
# initialize the trackbar window
vision_limestone.init_control_gui()

loop_time = time()
while(True):

    # get an updated image of the game
    # screenshot = wincap.get_screenshot()
    screenshot2 = wincap2.get_screenshot()
    # screenshot3 = wincap2.get_screenshot()
    # pre-process the image
    # output_image = vision_limestone.apply_hsv_filter(screenshot3)
    output_image2 = vision_limestone.apply_hsv_filter(screenshot2)
    # rectangles = vision_limestone.find(
    #     output_image, threshold=0.81, epsilon=0.5)
    rectangles2 = vision_limestone.find(
        output_image2, threshold=0.81, epsilon=0.5)
    # rectangles3 = vision_limestone.find(
    #     output_image2, threshold=0.81, epsilon=0.5)

    # display the processed image
    cv.imshow('Matches', screenshot2)

    # debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')
