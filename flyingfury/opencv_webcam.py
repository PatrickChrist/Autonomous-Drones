# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 23:29:04 2015

@author: patrickchrist
"""

import cv2
#import autopilot_agent

import cv
import autopilot_agent as aa

cam = cv2.VideoCapture(0) # Get the stream of your webcam
running = True
while running:    # get current frame of video    
    running, frame = cam.read()    
    if running:    
		# cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0), 2)   
        # print frame.shape # == 480,640
        size = frame.shape
        act = aa.action(frame,size[1],size[0],0,0,0,0,0,0,0,0,0)
        c = (int(act[1]*500),int(act[3]*500))
        print size[1]/2,size[0]/2
        cv2.line(frame,(size[1]/2,size[0]/2),((size[1]/2)+c[0],(size[0]/2)+c[1]),(255,0,0),2)        
        coord_hist = (act[1],act[3])
#        print (zap, phi, theta, gaz, yaw)

        cv2.imshow('frame', frame)        
        if cv2.waitKey(1) & 0xFF == 27:             # escape key pressed            
            running = False    
        else:        # error reading frame        
            print 'error reading video feed'
cam.release()
cv2.destroyAllWindows()
