# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 16:33:31 2015

@author: johannes
"""


import libardrone.libardrone as libardrone #import the libardone 
import numpy as np
import cv2 #import opencv

#drone=libardrone.ARDrone(1,1) #initalize the Drone Object 1=ardrone 2, 1=hd stream
running = True

centerX_prev = 0
centerY_prev = 0
radius_prev = 0
sameCircleCounter = 0
cap = cv2.VideoCapture(0)

while running:
    try:
        # This should be an numpy image array
        #drone.set_camera_view(True) 
    
        
      #webcam ansteuern über videocapture(0) oder so
      #pixelarray = drone.get_image() # get an frame form the Drone
        #pixelarray = drone.get_image() # get an frame form the Drone
        tmpret, tmpframeRGB = cap.read()
        if tmpframeRGB != None:
            frameRGB = tmpframeRGB
        #frameRGB = frameRGB[:, :, ::-1].copy()

        frame = cv2.cvtColor(frameRGB, cv2.COLOR_BGR2GRAY)

        #frameRGB = pixelarray[:, :, ::-1].copy()
        #frame = cv2.cvtColor(frameRGB, cv2.COLOR_RGB2GRAY);

          
      #if pixelarray != None: # check whether the frame is not empty
        if frame != None: # check whether the frame is not empty
                #reduce noise
                frametmp = cv2.medianBlur(frame,5)
                #find circles
                                #param1: higher treshold of canny edge detector
                #param2: accumulator treshold for circle center. The smaller it is, the more small circles are detected
                circles = cv2.HoughCircles(frametmp,3 ,1,800, param1=30,param2=40,minRadius=100,maxRadius=1000)                               
                
                radius = 0
                
                if circles != None:
                    
                    for i in circles[0,:]:
                        #draw the outer circle
                        cv2.circle(frameRGB,(i[0],i[1]),i[2],(0,255,0),2)
                        #draw the center of the circle
                        cv2.circle(frameRGB,(i[0],i[1]),2,(0,0,255),3)
                #get inner bounding box

                    if len(circles) == 1:
                        circle=circles[0][0]
                        radius = circle[2]
                        centerX = circle[0]
                        centerY = circle[1]
                        width = 2* np.sqrt(radius/2)
                        height = width
 
                        
                cv2.imshow('Drone', frameRGB) # show the frame"
                    
                #check whether the circle didnt change since the last frame
                
                if radius != 0:
                    diffRadius = np.abs(radius-radius_prev)
                    diffX=np.abs(centerX-centerX_prev)
                    diffY= np.abs(centerY-centerY_prev)
                    centerX_prev=centerX
                    centerY_prev=centerY
                    radius_prev=radius
                    print "diffRadius: " + str(diffRadius)+ ", diffX: " + str(diffX)+ ", diffY: " + str(diffY) 
                    if  diffRadius< 50 and  diffX< 25 and  diffY< 25:
                        sameCircleCounter+=1
                    else:
                        sameCircleCounter = 0
                    print "counter: " + str (sameCircleCounter)
                    if sameCircleCounter > 5:
                        print "Call Meanshift now!"
                        #left upper corner:
                        corner_x=centerX-width
                        cornter_Y=centerY-width
                        width = width
                        height = height
                        #return (corner_x,corner_y,width,height)
                
                k = cv2.waitKey(60) &0xFF
                if k == 27: #stop with esc
                    cap.release()
                    cv2.destroyAllWindows()
                    running = False

    except:
        print "Failed"
        
        
