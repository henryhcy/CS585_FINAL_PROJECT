import sys  # System bindings
import cv2  # OpenCV bindings
import numpy as np
from PIL import Image
import os
if __name__ == "__main__":
    # read in
    image_good = cv2.imread('normal.jpg',0)
##    image_bad = cv2.imread('src1.png', 0)

    # Adaptive Threshold
    good_saw = cv2.adaptiveThreshold(image_good, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 5)
    cv2.imwrite('good.png',good_saw)
##    bad_saw = cv2.adaptiveThreshold(image_bad, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 25, 10)
##    cv2.imwrite('bad.png',bad_saw)

    # Morphology
    erode_kernel = np.ones((3, 3), np.uint8)
    dilate_kernel = np.ones((2, 2), np.uint8)

    erosion1 = cv2.erode(good_saw, erode_kernel, iterations=1)
    dilation1 = cv2.dilate(erosion1, dilate_kernel, iterations=1)
    cv2.imwrite('morpho_good.png',dilation1)

##    erosion2 = cv2.erode(bad_saw, erode_kernel, iterations=1)
##    dilation2 = cv2.dilate(erosion2, dilate_kernel, iterations=1)
##    cv2.imwrite('morpho_bad.png', dilation2)
##
    contours_good, hierarchy_good = cv2.findContours(dilation1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
##    im_bad, contours_bad, hierarchy_bad = cv2.findContours(dilation2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    test_good = cv2.imread('good.png', 1)
##    test_bad = cv2.imread('src1.png', 1)
    cv2.drawContours(test_good, contours_good, -1, (0, 255, 0), 1)
    cv2.imwrite('good_contour.png', test_good)

##    cv2.drawContours(test_bad, contours_bad, -1, (0, 255, 0), 1)
##    cv2.imwrite('bad_contour.png', test_bad)
