import cv2 as cv
import numpy as np
import os
from time import time, sleep
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import grab_object_preset
from actions import Movement_Handler


def main_loop():
    # Allow 3 seconds to open the game window
    sleep(3)

    # Change the working directory to the folder this script is in.
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Initialise the actions object
    movement = Movement_Handler(test_mode=False)

    # Grab the gamename from the text file
    with open("gamename.txt") as f:
        gamename = f.readline()

    # The next block of code is for detecting the object in question
    object_filter, object_custom_rect = grab_object_preset(
        object_name="other_player_map_loc")
    # initialize the WindowCapture class for object detection
    object_wincap = WindowCapture(
        gamename, object_custom_rect)
    # initialize the Vision class
    object_vision = Vision('otherplayer.jpg')

    # This next block of code is for detecting the current player position
    # It uses the same part of the screen as the other player bit above
    # So no need to grab another wincap object
    player_filter, player_custom_rect = grab_object_preset(
        object_name="player_map_loc")
    player_vision = Vision('playerv2.jpg')
    player_vision_inverted = Vision("playerv2_inv.jpg")

    # This block of code is for detecting if in a dungeon or not
    dunchk_filter, dunchk_custom_rect = grab_object_preset(
        object_name="dungeon_check")
    # This is only for testing and fixing the 150% screen scaling I have
    dunchk_wincap = WindowCapture(
        gamename, dunchk_custom_rect)
    dunchk_vision = Vision('dunchk_67.jpg')

    # Start the movement bot
    movement.movement_start()

    loop_time = time()
    while(True):

        # get an updated image of the game at specified area
        dunchk_screenshot = dunchk_wincap.get_screenshot()
        # pre-process the image to help with detection
        dunchk_output_image = dunchk_vision.apply_hsv_filter(
            dunchk_screenshot, dunchk_filter)
        # do object detection, this time grab the points
        dunchk_rectangles = dunchk_vision.find(
            dunchk_output_image, threshold=0.27, epsilon=0.5)

        # then if currently in a dungeon search for object
        if len(dunchk_rectangles) == 1:
            # get an updated image of the game at map loc
            screenshot = object_wincap.get_screenshot()
            # then try to detect the other player
            output_image = object_vision.apply_hsv_filter(
                screenshot, object_filter)
            # do object detection, this time grab the points
            rectangles = object_vision.find(
                output_image, threshold=0.41, epsilon=0.5)
            # draw the detection results onto the original image
            points = object_vision.get_click_points(rectangles)
            if len(points) == 1:
                output_image = object_vision.draw_crosshairs(
                    screenshot, points)
                # If there is only one value found
                # i.e. no false positives and players are not on top of each other
                # Then grab the current player position and feed it in as coords
                player_image = player_vision.apply_hsv_filter(
                    screenshot, player_filter)
                player_rectangles = player_vision.find(
                    player_image, threshold=0.41, epsilon=0.5)
                player_points = player_vision.get_click_points(
                    player_rectangles)
                if len(player_points) == 1:
                    output_image = object_vision.draw_crosshairs(
                        output_image, player_points)
                    relx = points[0][0]-player_points[0][0]
                    rely = player_points[0][1]-points[0][1]
                    movement.movement_update_xy(relx, rely)
                else:
                    # Check to see if the image is just inverted
                    # Seem to have trouble if it is upside down
                    # Probably a function that can solve this problem somewhere
                    inverted_player_image = player_vision.apply_hsv_filter(
                        screenshot, player_filter)
                    inverted_player_rectangles = player_vision.find(
                        inverted_player_image, threshold=0.41, epsilon=0.5)
                    inverted_player_points = player_vision.get_click_points(
                        inverted_player_rectangles)
                    if len(inverted_player_points) == 1:
                        output_image = object_vision.draw_crosshairs(
                            output_image, inverted_player_points)
                        relx = points[0][0]-inverted_player_points[0][0]
                        rely = inverted_player_points[0][1]-points[0][1]
                        movement.movement_update_xy(relx, rely)
                    else:
                        movement.movement_update_xy(0, 0)
            else:
                # Clear all keypresses
                movement.movement_update_xy(0, 0)
            # cv.imshow('Matches', screenshot)
        else:
            movement.movement_update_xy(0, 0)
            sleep(0.5)

        # cv.imshow("Dunchk", dunchk_output_image)
        # debug the loop rate
        #print('FPS {}'.format(1 / (time() - loop_time)))
        #loop_time = time()

        # press 'q' with the output window focused to exit.
        # waits 1 ms every loop to process key presses
        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            movement.movement_stop()
            break
    print('Exiting Script')


if __name__ == "__main__":
    main_loop()
