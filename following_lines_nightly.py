# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 13:06:11 2015

@author: broen
"""

import libardrone.libardrone as libardrone
import cv2
import numpy as np
import time
import math


#variables
running = True
flying = False
loop = False
line_in_sight = False
# operational
speed_ratio = 50 #speed 1/n
angle_change = 0.005 #constant to navigate towards the line on x-axis
gain_x = 0.3 #horizontal gain
gain_z = 0.3 #vertical_gain
# optimum
optimum_x = 160 #center in the middle of 320px frame
optimum_z = 650 #keep height at 80cm
#image buffer
buffer_counter = 0
buffer_distance = 10
buffer_image = None
#hovering
hovered = False
threshold_x = 40

hover_timer = time.time()

# init da drone
drone=libardrone.ARDrone(1,1) #initalize the Drone Object
drone.set_camera_view(0)
print 'battery:', drone.navdata[0]['battery']

    
while running:
    try:
# get image
        pixelarray = drone.get_image() # get an frame form the Drone
        
        buffer_counter += 1
#        if time.time() - buffer_time >= 1:
#            #print "fps:", buffer_counter
#            buffer_counter = 0
#            buffer_time = time.time()
        # check whether the frame is not empty, only take every nth picture
        #if pixelarray != None and buffer_counter % buffer_distance == 0:
        if pixelarray != None and not (np.array(pixelarray) == np.array(buffer_image)).all():
            buffer_image = pixelarray
            frame = pixelarray[:, :, ::-1].copy() #convert to a frame
            resized = cv2.resize(frame, (320, 180)) #resize image
            
            # display the image
            
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
            if lines is not None and loop:
#TODO search for the line
            
                for rho,theta in lines[0]:
                
                    a = np.cos(theta)
                    b = np.sin(theta)
                    #x = a * rho
                    #y = b * rho
                    #rho = abs(rho)
                    if rho > 180:
                        a_prime = np.cos(theta + math.pi / 4)
                        b_prime = np.sin(theta + math.pi / 4)
                    else:
                        a_prime = np.cos(theta - math.pi / 4)
                        b_prime = np.sin(theta - math.pi / 4)
                    #a_new = abs(a) + a_prime * angle_change * (rho / 160 - 1)
                    #b_new = b + b_prime * angle_change * (rho / 160 - 1)
                    #print 'theta:', theta, 'rho', rho 
                    print rho
                    
                    if theta < math.pi / 2:
                        b = -b
                
                    #w, h, d = frame.shape
            
                    lr = b / speed_ratio
                    fb = a / speed_ratio
                    
# inputs
                    theta = abs(theta)
                    slope = b / a
                    z = drone.navdata[0]['altitude']
# corrections
                    #check speed maybe?                    
                    #correct_x = (x - optimum_x) / optimum_x * gain_x
                    correct_z = (optimum_z - z) / optimum_z * gain_z
                    
# print to console
                    
                    #print_x = 'right   ' if correct_x > 0 else 'left    '
                    #print_z = 'up    ' if correct_z > 0 else 'down  '
                    #print print_x, correct_x, print_z, correct_z
                    #print 'speed:', speed, 'x:', correct_x, 'up:', correct_z, 'rotate:', correct_r
#call the drone
                    drone.at(libardrone.at_pcmd, True, -float(lr), -float(fb), correct_z, 0)

#keyboard controls
                    
            cv2.imshow('Drone', resized) # show the frame                    
                    
            k = cv2.waitKey(33)
            if k == 27: #stop with esc
                running = False
            elif k == 32: # start/stop with space bar
                if flying:
                    drone.land()
                else:
                    drone.takeoff()
                flying = not flying
                # wasd for front/back/left/right 
            elif k == ord('a'): 
                drone.move_left()
            elif k == ord('d'):
                drone.move_right()
            elif k == ord('w'):
                drone.move_forward()
            elif k == ord('s'):
                drone.move_backward()
                
            # arrow keys for up/down/rotate
            elif k == 63232:
                drone.move_up()
            elif k == 63233:
                drone.move_down()
            elif k == 63234:
                drone.turn_left()
            elif k == 63235:
                drone.turn_right()
                
            elif k == ord('q'):
                drone.at(libardrone.at_pcmd, True, 0, -0.2, 0, 0)
            
            #hover on h
            elif k == ord('h'):
                drone.hover()            
            # start with l
            elif k == ord('l'):
                loop = True 
                hover_timer = time.time()
            # print height with h
            elif k == ord('p'):
                print drone.navdata[0]['altitude'] 
    except ValueError as e:
        print e