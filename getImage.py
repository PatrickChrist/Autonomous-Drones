# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 18:09:05 2015

@author: patrickchrist
"""

import libardrone.libardrone as libardrone #import the libardone 
import cv2 #import opencv

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
    except:
        print "Failed"