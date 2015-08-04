# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 17:36:03 2015

@author: johannes
"""


import libardrone.libardrone as libardrone #import the libardone 
import numpy as np
import cv2 #import opencv

#drone=libardrone.ARDrone(1,1) #initalize the Drone Object 1=ardrone 2, 1=hd stream
running = True
cap = cv2.VideoCapture(0)




while running:
    try:
        # This should be an numpy image array
        #drone.set_camera_view(True) 
    
        
        tmpret, tmpframeRGB = cap.read()
        if tmpframeRGB != None:
            frameRGB = tmpframeRGB
        else:
            print "couldnt read from webcam"
        #frameRGB = frameRGB[:, :, ::-1].copy()

        
        if frameRGB != None: # check whether the frame is not empty
            frame = cv2.cvtColor(frameRGB, cv2.COLOR_BGR2GRAY)
            cv2.imshow('Drone', frameRGB) # show the frame"
        else:
            print "no frame"
            
            
        k = cv2.waitKey(60) &0xFF
        if k == 27: #stop with esc
            cap.release()
            cv2.destroyAllWindows()
            running = False
            break
    except:
        print "Failed"