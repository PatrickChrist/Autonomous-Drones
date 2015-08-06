# -*- coding: utf-8 -*-
"""
Created on Wed Aug 05 09:21:03 2015

@author: Valentin
"""

import cv2
import numpy as np
import libardrone.libardrone as libardrone
import threading
import time

import manual_control_helpers as mch

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
        
    return decision


def print_action(d):
    if d == 0:
        print "vor"
    elif d == -1:
        print "links drehen"
    elif d == 1:
        print "rechts drehen"
    elif d == 3:
        print "links fliegen"
    elif d == -3:
        print "rechts fliegen"
    else:
        print "nichts"
        
def do_action(d):
    if d == 0:
        mch.forward()
    elif d == -1:
        mch.tLeft()
    elif d == 1:
         mch.tRight()
    elif d == 3:
        mch.left()
    elif d == -3:
        mch.right()
    else:
        mch.upward()
        
        
def webcam_test():
    
    cap = cv2.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
            # Display the resulting frame
        #if frame != None:
        cv2.imshow('frame',frame)
        
        k = cv2.waitKey(1)
        
        if k == ord('q'):
            break
        
        if k == ord('c'):
            print 'capturing!'
            cv2.imwrite("test.jpg",frame) 
            
            # When everything done, release the capture
        cap.release()
        cv2.destroyAllWindows()

def drone_test():
    global drone
    
    drone = libardrone.ARDrone(1, 1)
    drone.set_camera_view(0)
    #if online:
    drone.takeoff()
    time.sleep(2)    
    
    thread = threading.Thread(target=decision_loop, args=("I'ma", "thread"))
    thread.start()


running = True
drone = None
def decision_loop(a, b):
    global running
    global drone
    while running:
        img = drone.get_image()
        mch.show_img(img)

        d = decision(img)
        do_action(d)
        
    cv.destroyAllWindows()
        
        
        
        
        
        