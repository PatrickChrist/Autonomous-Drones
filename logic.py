# -*- coding: utf-8 -*-
"""
Created on Thu Aug 06 09:13:47 2015

@author: Valentin
"""

import cv2

def decision(img):
    
    resized = cv2.resize(img, (320, 180))

    # Convert BGR to HSV
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_red = np.array([160,50,50], dtype=np.uint8)
    upper_red = np.array([180,255,255], dtype=np.uint8)

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(resized,resized, mask= mask)
    
    blur = cv2.GaussianBlur(res,(15,15),0)

    ##line detection

    #convert colors
    gray = cv2.cvtColor(blur, cv2.COLOR_HSV2BGR)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(blur,50,150,apertureSize = 3)
    
    decision = 0

    #find lines
    lines = cv2.HoughLines(edges,1,np.pi/180,50)
    
    if lines is None:
        decision = 2
    else:
        for rho,theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            
            x = a * rho
            #print "dX:", a
            #print "dY:", b
            #print "Steigung:", b / a
            steigung = b / a
            if steigung > 0.2:
                decision = 1
            elif steigung < -0.2:
                decision = -1
            elif x > 260:
                decision = 3
            elif x < 60:
                decision = -3
            else:
                decision = 0
        
    return decision