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

# Grab the gamename from the text file
with open("gamename.txt") as f:
    gamename = f.readline()

filter, custom_rect = grab_object_preset("player_map_loc", big_map=True)
# WindowCapture.list_window_names()
# initialize the WindowCapture class
# wincap = WindowCapture(gamename)
wincap2 = WindowCapture(gamename, custom_rect)

# initialize the Vision class
vision_limestone = Vision('dunchk_67.jpg')
# initialize the trackbar window
vision_limestone.init_control_gui()

loop_time = time()
count100 = 0
samples = []
while(True):
    count100 += 1
    # get an updated image of the game
    # screenshot = wincap.get_screenshot()
    screenshot2 = wincap2.get_screenshot()
    screenshot3 = wincap2.get_screenshot()
    screenshot4 = wincap2.get_screenshot()
    screenshot5 = wincap2.get_screenshot()
    screenshot6 = wincap2.get_screenshot()
    screenshot7 = wincap2.get_screenshot()
    screenshot8 = wincap2.get_screenshot()
    screenshot9 = wincap2.get_screenshot()
    screenshot10 = wincap2.get_screenshot()
    screenshot11 = wincap2.get_screenshot()
    # pre-process the image
    # output_image = vision_limestone.apply_hsv_filter(screenshot3)
    output_image2 = vision_limestone.apply_hsv_filter(screenshot2)
    output_image2 = vision_limestone.apply_hsv_filter(screenshot3)
    output_image2 = vision_limestone.apply_hsv_filter(screenshot4)
    output_image2 = vision_limestone.apply_hsv_filter(screenshot5)
    output_image2 = vision_limestone.apply_hsv_filter(screenshot6)
    output_image2 = vision_limestone.apply_hsv_filter(screenshot7)
    output_image2 = vision_limestone.apply_hsv_filter(screenshot8)
    output_image2 = vision_limestone.apply_hsv_filter(screenshot9)
    output_image2 = vision_limestone.apply_hsv_filter(screenshot10)
    output_image2 = vision_limestone.apply_hsv_filter(screenshot11)
    # rectangles = vision_limestone.find(
    #     output_image, threshold=0.81, epsilon=0.5)
    # rectangles2 = vision_limestone.find(
    #     output_image2, threshold=0.81, epsilon=0.5)
    # rectangles3 = vision_limestone.find(
    #     output_image2, threshold=0.81, epsilon=0.5)

    # display the processed image
    cv.imshow('Matches', screenshot2)

    # debug the loop rate
    # print('FPS {}'.format(1 / (time() - loop_time)))
    if count100 % 100 == 0:
        # print("100 frame time: {}".format(time()-loop_time))
        samples.append(time()-loop_time)
        loop_time = time()
    if count100 % 3000 == 0:
        break
    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
print("Average of 30 samples: {}".format(sum(samples)/len(samples)))
print('Done.')
