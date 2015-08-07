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

"""
    controls:
        
        space:      take-off / land
        l:          start line detection loop
        h:          hover
        p:          print altitude
        
        w:          forward         
        a:          left
        s:          down
        d:          right
        
        up:         up
        down:       down
        left:       rotate left
        right:      rotate right
"""

"""
    adjust speed_ratio for correction speed changes 
    higher number results in slower speed
    max speed at speed_ratio = 1
    30 turned out to give solid results 
"""
speed_ratio = 30 #speed 1/n
"""
    rotor_speed defines takes floats from 0.0 to 1.0
"""
rotor_speed = 0.2

"""
    these two HSV values define the color range to detect
    this version uses a red line
"""
lower_color = np.array([160,50,50], dtype=np.uint8)
upper_color = np.array([180,255,255], dtype=np.uint8)


# initial startup values
running = True
flying = False
loop = False
hovered = False
line_in_sight = False
# navigation constant towards the line
angle_change = 0.00001
gain_x = 0.3 #horizontal gain
gain_z = 0.3 #vertical_gain
 #center in the middle of 320px frame
optimum_x = 160
#keep height at 65cm
optimum_z = 650
buffer_image = None
#line threshold
threshold_x = 40

hover_timer = time.time()

# init da drone
drone=libardrone.ARDrone(1,1) #initalize the Drone Object
drone.set_camera_view(0)
print 'battery:', drone.navdata[0]['battery']

    
while running:
    try:
        #get an image from the drone
        pixelarray = drone.get_image()
        # buffer
        if pixelarray != None and not (np.array(pixelarray) == np.array(buffer_image)).all():
            buffer_image = pixelarray
             #convert to a frame
            frame = pixelarray[:, :, ::-1].copy()
             #resize image
            resized = cv2.resize(frame, (320, 180))
            # image conversion 
            #convert BGR to HSV
            hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
            # threshold the HSV image to get only blue colors
            mask = cv2.inRange(hsv, lower_color, upper_color)
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
                for rho,theta in lines[0]:    
                    a = np.cos(theta)
                    b = np.sin(theta)
                    x = a * rho
                    y = b * rho
                    delta_x = x/180 -1
                    if theta < math.pi / 2:
                        b = -b
                    # x component
                    x_correction = delta_x * angle_change
                    x_lr = x_correction * b
                    x_fb = x_correction * a
                    lr = str(b / speed_ratio)
                    fb = str(abs(a) / speed_ratio)
                    # inputs
                    slope = b / a
                    z = drone.navdata[0]['altitude']
                    # corrections
                    correct_x = (x - optimum_x) / optimum_x * gain_x
                    correct_z = (optimum_z - z) / optimum_z * gain_z
                    #call the drone
                    drone.at(libardrone.at_pcmd, True, -float(lr), -float(fb), correct_z, 0)
                    
            #user interface
            drone.set_speed(rotor_speed)
            #show the frame 
            cv2.imshow('Drone', resized)                   
            #keyboard controls
            k = cv2.waitKey(33)
            if k == 27: #stop with esc
                running = False
            elif k == 32: # start/land with space bar
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