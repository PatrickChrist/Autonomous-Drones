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
speed_ratio = 40 #speed 1/n
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

hover_timer = time.time()

# init da drone
drone=libardrone.ARDrone(1,1) #initalize the Drone Object
print 'battery:', drone.navdata[0]['battery']

# calculate the center of the line
def middle(start, end, a, b):
    x0, y0 = start
    xn, yn = end
    in_range = None
    num_in_range = 0
    while x0 < xn and y0 < yn:
        x0 += a
        y0 += b
        if x0 >= 0 and y0 >= 0 and x0 <= 320 and y0 <= 180:
            if in_range == None:
                in_range = (x0, y0)
            num_in_range += 1
    xl, yl = in_range
    return (xl + (-b) * (num_in_range / 2), yl + a * (num_in_range / 2))
        
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
            
                if time.time() - hover_timer < 5:
                    for rho,theta in lines[0]:
                    
                        a = np.cos(theta)
                        b = np.sin(theta)
                        x = a * rho
                        
                        x = a * rho
                        # fake theta
                        theta_delta = 0
                        if x < optimum_x - 20:
                            theta += angle_change
                            theta_delta = -angle_change
                        elif x > optimum_x + 20:
                            theta += angle_change
                            theta_delta = angle_change
                        else:
                            drone.hover()
                            time.sleep(1)
                        a = np.cos(theta)
                        b = np.sin(theta)
                        
                        if theta < math.pi / 2:
                            b = -b
                    
                        w, h, d = frame.shape
                
                        #cv2.line(resized, (int(w/2), int(h/2)), (int(w/2+b*1000), int(h/2-a*1000)), (255, 0, 255))
                        lr = str(b / speed_ratio)
                        rb = str(abs(a) / speed_ratio)
                        font = cv2.FONT_HERSHEY_SIMPLEX
                        #cv2.putText(resized,'lr: ' + lr,(10,70), font, 1,(255,255,255),2)
                        #cv2.putText(resized,'rb: ' + rb,(10,120), font, 1,(255,255,255),2)
                        #cv2.putText(resized,'th: ' + str(theta_delta),(10,170), font, 1,(255,255,255),2)
                        resized = cv2.line(resized,(x,0),(x,180),(100,200,170),5)
    # inputs
                        
                        slope = b / a
                        z = drone.navdata[0]['altitude']
    # corrections
                        #check speed maybe?                    
                        correct_x = (x - optimum_x) / optimum_x * gain_x
                        
                        correct_z = (optimum_z - z) / optimum_z * gain_z
    # print to console
                        
                        print_x = 'right   ' if correct_x > 0 else 'left    '
                        print_z = 'up    ' if correct_z > 0 else 'down  '
                        print print_x, correct_x, print_z, correct_z
                        #rint 'speed:', speed, 'x:', correct_x, 'up:', correct_z, 'rotate:', correct_r
    #call the drone
                        drone.at(libardrone.at_pcmd, True, -float(lr), -float(rb), correct_z, 0)
                else:
                    drone.hover()
                    hover_timer = time.time()
                    time.sleep(1)
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
            #speed adjustment on i & o
            elif k == ord('i'):
                speed += 0.05
                print 'speed:', -speed
            elif k == ord('o'):
                speed -= 0.05
                print 'speed:', -speed
            # start with l
            elif k == ord('l'):
                loop = True 
                hover_timer = time.time()
            # print height with h
            elif k == ord('p'):
                print drone.navdata[0]['altitude'] 
    except ValueError as e:
        print e