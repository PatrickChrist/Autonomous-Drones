# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 13:06:11 2015

@author: broen
"""

import libardrone.libardrone as libardrone
import cv2
import numpy as np

drone=libardrone.ARDrone(1,1) #initalize the Drone Object
running = True
while running:
    try:
        # This should be an numpy image array
        pixelarray = drone.get_image() # get an frame form the Drone
        if pixelarray != None: # check whether the frame is not empty
            frame = pixelarray[:, :, ::-1].copy() #convert to a frame
            # Display the Image
            cv2.imshow('Drone', frame) # show the frame
            if cv2.waitKey(1) & 0xFF == 27: #stop with esc
            # escape key pressed
                running = False
            # image conversion
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
            
            blur = cv2.GaussianBlur(res,(15,15),0)
    except:
        print "no image"
        
        
        """
        img = img[:, :, ::-1].copy()
    resized = cv2.resize(img, (320, 180))

    

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
        
    return decision"""