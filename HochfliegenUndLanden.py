# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 19:21:28 2015

@author: broen
"""


import cv2
import numpy as np
import libardrone.libardrone as libardrone
import threading
import time

def show(a, b):
    global drone
    img = drone.get_image()
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def show_img(img):
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def navdata(a, b):
    global drone;
    a = 0
    while a < 10:
        if drone.get_navdata()[0]['altitude'] < 2000:
            drone.move_up()
        else:
            drone.hover()
        a = a + 1
        time.sleep(1)
    drone.hover()

drone = libardrone.ARDrone(1, 1)
drone.set_camera_view(0)

def decision(img):
    
    resized = cv2.resize(img, (320, 180))

    # Convert BGR to HSV
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_red = np.array([125,50,50], dtype=np.uint8)
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
            #print "dX:", a
            #print "dY:", b
            #print "Steigung:", b / a
            steigung = b / a
            if steigung > 0.2:
                decision = 1
            elif steigung < -0.2:
                decision = -1
            else:
                decision = 0
        
    return decision
    
drone.takeoff()

def right():
    global drone
    drone.move_right()
    time.sleep(1)
    drone.hover()
    
def left():
    global drone
    drone.move_left()
    time.sleep(1)
    drone.hover()
    
def tRight():
    global drone
    drone.turn_right()
    time.sleep(1)
    drone.hover()
    
def tLeft():
    global drone
    drone.turn_left()
    time.sleep(1)
    drone.hover()
    
def forward():
    global drone
    drone.move_forward()
    time.sleep(1)
    drone.hover()
    
def upward():
    global drone
    drone.move_up()
    time.sleep(1)
    drone.hover()
    
def downward():
    global drone
    drone.move_down()
    time.sleep(1)
    drone.hover()
    
def img():
    global drone
    show_img(drone.get_image())

def one_action():
    global drone
    d = decision(drone.get_image())
    if d == 0:
        forward()
    elif d == -1:
        tLeft()
    elif d == 1:
        tRight()
    else:
        upward()
    