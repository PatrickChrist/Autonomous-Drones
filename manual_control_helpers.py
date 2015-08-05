# -*- coding: utf-8 -*-
"""
Created on Tue Aug 04 21:11:26 2015

@author: Valentin
"""

import cv2
import numpy as np
import libardrone.libardrone as libardrone
import threading
import time

action_duration = 0.5

def show_img(img):
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def right():
    global drone
    global action_duration
    drone.move_right()
    time.sleep(action_duration)
    drone.hover()
    
def left():
    global drone
    global action_duration
    drone.move_left()
    time.sleep(action_duration)
    drone.hover()
    
def tRight():
    global drone
    global action_duration
    drone.turn_right()
    time.sleep(action_duration)
    drone.hover()
    
def tLeft():
    global drone
    global action_duration
    drone.turn_left()
    time.sleep(action_duration)
    drone.hover()
    
def forward():
    global drone
    global action_duration
    drone.move_forward()
    time.sleep(action_duration)
    drone.hover()
    
def upward():
    global drone
    global action_duration
    drone.move_up()
    time.sleep(action_duration)
    drone.hover()
    
def down():
    global drone
    global action_duration
    drone.move_down()
    time.sleep(action_duration)
    drone.hover()
    
def back():
    global drone
    global action_duration
    drone.move_backward()
    time.sleep(action_duration)
    drone.hover()
    
    
def img():
    global drone
    show_img(drone.get_image())
