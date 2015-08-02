# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 23:27:54 2015

@author: patrickchrist
"""

import cv2
# Creates a numpy.ndarray object 
img = cv2.imread(“path to your file", cv2.IMREAD_COLOR) 

# Creates a window (title = ‘Your Image!’) and displays img in it.
cv2.imshow(‘Your Image', img)

# Waits for any key to be pressed.
cv2.waitKey(0)
# Destroys all windows.
cv2.destroyAllWindows()
