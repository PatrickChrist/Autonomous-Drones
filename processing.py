# -*- coding: utf-8 -*-
"""
Created on Tue Aug 04 15:19:03 2015

@author: Valentin
"""

import cv2
import numpy as np

#cap = cv2.VideoCapture(0)


    # Take each frame
frame = cv2.imread('img.png', 1)
resized = cv2.resize(frame, (320, 180))

# Convert BGR to HSV
hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

# define range of blue color in HSV
lower_red = np.array([160,50,50], dtype=np.uint8)
upper_red = np.array([180,255,255], dtype=np.uint8)

# Threshold the HSV image to get only blue colors
mask = cv2.inRange(hsv, lower_red, upper_red)

# Bitwise-AND mask and original image
res = cv2.bitwise_and(resized,resized, mask= mask)

##line detection

#vars
minLineLength = 10
maxLineGap = 40

#convert colors
gray = cv2.cvtColor(res, cv2.COLOR_HSV2BGR)
gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)

#find lines
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
print lines
for x1,y1,x2,y2 in lines[0]:
    cv2.line(res,(x1,y1),(x2,y2),(0,255,0),2)
    
#save lines
#cv2.imwrite('lines.jpg',res)

cv2.imshow('frame',frame)
#cv2.imshow('mask',mask)
cv2.imshow('res',gray)

cv2.waitKey(0)

cv2.destroyAllWindows()