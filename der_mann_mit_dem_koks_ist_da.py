# -*- coding: utf-8 -*-
"""
Created on Tue Aug 04 17:46:50 2015

@author: Valentin
"""


import cv2
import numpy as np
import libardrone.libardrone as libardrone
import threading
import time

#cap = cv2.VideoCapture(0)

running = False
online = False
drone = None

def show(img):
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
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
        decision = 0
    else:
        for rho,theta in lines[0]:
            a = np.cos(theta)
            b = np.sin(theta)
            print "dX:", a
            print "dY:", b
            print "Steigung:", b / a
            steigung = b / a
            if steigung > 0.2:
                decision = 15
            elif steigung < -0.2:
                decision = -15
        
    return decision
    
def drone_action_left(online):
    if online:
        drone.hover()
        drone.turn_left()
        time.sleep(0.5)
        drone.hover()
    else:
        print "turning right"

def drone_action_right(online):
    if online:
        drone.hover()
        drone.turn_right()
        time.sleep(0.5)
        drone.hover()
    else:
        print "turning left"
        
def drone_action_down(online):
    if online:
        drone.move_down();
        time.sleep(0.1)
        drone.hover()
    else:
        print "moving down"
        
def drone_action_up(online):
    if online:
        drone.move_up()
        time.sleep(0.1)
        drone.hover()
    else:
        print "moving up"
    
    
def drone_control(a, b):
    global running  
    global online
    global drone
    
    drone = libardrone.ARDrone(1, 1)
    if online:
        drone.takeoff()
        time.sleep(2)
    
    #get image and decision loop
    running = True
    while running:
        try:
            
            #first make sure the height is okay
            altitude = drone.get_navdata()['altitude']
            if altitude > 1200:
                drone_action_down(online)
            elif altitude < 500:
                drone_action_up(online)
            
            pixelarray = drone.get_image() 
            if pixelarray != None:
                frame = pixelarray[:, :, ::-1].copy()
                cv2.imshow('Drone', frame)
                
                turnDecision = decision(frame)
                
                if turnDecision < -10:
                    drone_action_left(online)
                elif turnDecision > 10:
                    drone_action_right(online)
                else:
                    #drone.move_forward()
                    print "moving forward"
                if cv2.waitKey(1) & 0xFF == 27:
                    running = False
                    
        except:
            print "Failed"
            
def webcam_control(a, b):
    
    cam = cv2.VideoCapture(0) # Get the stream of your webcam
    webcamRunning = True
    while webcamRunning:    # get current frame of video    
        webcamRunning, frame = cam.read()    
        if webcamRunning:    
            # cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0), 2)            
            print decision(frame)
            cv2.imshow('frame', frame)
            
            if cv2.waitKey(1) & 0xFF == 27:             # escape key pressed            
                webcamRunning = False    
        else:        # error reading frame        
            print 'error reading video feed'
                
    cam.release()
    cv2.destroyAllWindows()

    

thread = threading.Thread(target=drone_control, args=("I'ma", "thread"))
thread.start()