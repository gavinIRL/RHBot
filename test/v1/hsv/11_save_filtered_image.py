import cv2 as cv
from hsvfilter import HsvFilter, grab_object_preset
import numpy as np
import os


class SaveFilteredImage():

    def shift_channel(self, c, amount):
        if amount > 0:
            lim = 255 - amount
            c[c >= lim] = 255
            c[c < lim] += amount
        elif amount < 0:
            amount = -amount
            lim = amount
            c[c <= lim] = 0
            c[c > lim] -= amount
        return c

    def save_and_convert(self, filter, existing_image, save_image):
        img = cv.imread(existing_image, cv.IMREAD_UNCHANGED)
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        hsv_filter = filter
        # add/subtract saturation and value
        h, s, v = cv.split(hsv)
        s = self.shift_channel(s, hsv_filter.sAdd)
        s = self.shift_channel(s, -hsv_filter.sSub)
        v = self.shift_channel(v, hsv_filter.vAdd)
        v = self.shift_channel(v, -hsv_filter.vSub)
        hsv = cv.merge([h, s, v])

        # Set minimum and maximum HSV values to display
        lower = np.array([hsv_filter.hMin, hsv_filter.sMin, hsv_filter.vMin])
        upper = np.array([hsv_filter.hMax, hsv_filter.sMax, hsv_filter.vMax])
        # Apply the thresholds
        mask = cv.inRange(hsv, lower, upper)
        result = cv.bitwise_and(hsv, hsv, mask=mask)

        # convert back to BGR for imshow() to display it properly
        img = cv.cvtColor(result, cv.COLOR_HSV2BGR)
        cv.imwrite(save_image, img)


os.chdir(os.path.dirname(os.path.abspath(__file__)))
filter, _ = grab_object_preset(
    object_name="tough_enemy_tag")
sfi = SaveFilteredImage()
existing_image = "toughenemytagonly100.jpg"
save_image = "toughenemytagonly100filt.jpg"
sfi.save_and_convert(filter, existing_image, save_image)
