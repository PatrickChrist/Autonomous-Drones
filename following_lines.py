# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 13:06:11 2015

@author: broen
"""

import libardrone.libardrone as libardrone
import cv2
import numpy as np

#variables
running = True
flying = False
# operational
speed = 0.1 #forward movement
gain_x = 0.1 #horizontal gain
gain_z = 0.2 #vertical_gain
gain_r = 0.1 #rotation gain
# optimum
optimum_x = 160 #center in the middle of 320px frame
optimum_z = 800 #keep height at 80cm
optimum_r = 0 #no rotation por favor

# init da drone
drone=libardrone.ARDrone(1,1) #initalize the Drone Object
print 'battery:', drone.navdata[0]['battery']

while running:
    try:
# get image
        pixelarray = drone.get_image() # get an frame form the Drone
        if pixelarray != None: # check whether the frame is not empty
            frame = pixelarray[:, :, ::-1].copy() #convert to a frame
            resized = cv2.resize(frame, (320, 180)) #resize image
            # display the image
            cv2.imshow('Drone', resized) # show the frame
# image conversion 
            #convert BGR to HSV
            hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
            # define range of blue color in HSV
            lower_red = np.array([160,50,50], dtype=np.uint8)
            upper_red = np.array([180,255,255], dtype=np.uint8)
            # threshold the HSV image to get only blue colors
            mask = cv2.inRange(hsv, lower_red, upper_red)
            # bitwise-AND mask and original image
            res = cv2.bitwise_and(resized,resized, mask= mask)
            blur = cv2.GaussianBlur(res,(15,15),0)
#line detection
            #convert colors
            gray = cv2.cvtColor(blur, cv2.COLOR_HSV2BGR)
            gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(blur,50,150,apertureSize = 3)
            #find lines
            lines = cv2.HoughLines(edges,1,np.pi/180,50)
# decisions
            if lines is None:
                #TODO search for the line
                print 'no line in sight'
            else:
                for rho,theta in lines[0]:
                    a = np.cos(theta)
                    b = np.sin(theta)
# inputs
                    x = a * rho
                    slope = b / a
                    z = drone.navdata[0]['altitude']
# corrections
                    #check speed maybe?                    
                    correct_x = (optimum_x - x) / optimum_x * gain_x
                    correct_z = (optimum_z - z) / optimum_z * gain_z
                    correct_r = (optimum_r - slope) * gain_r
# print to console
                    
                    print_x = 'right   ' if correct_x > 0 else 'left    '
                    print_z = 'up    ' if correct_z > 0 else 'down  '
                    print_r = 'rotate right' if correct_r > 0 else 'rotate left '
                    print print_x + print_z + print_r
                    #print 'speed:', speed, 'x:', correct_x, 'up:', correct_z, 'rotate:', correct_r
#call the drone
                    drone.at(drone.at_pcmd, correct_x, speed, correct_z, correct_r)
#keyboard controls
            k = cv2.waitKey(33)
            if k == 27: #stop with esc
                running = False
            elif k == 32: # start/stop with space bar
                if flying:
                    drone.land()
                else:
                    drone.takeoff()
                flying = not flying
    except:
        print ""
        
