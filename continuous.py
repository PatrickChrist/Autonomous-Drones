# -*- coding: utf-8 -*-
"""
Created on Thu Aug 06 09:12:20 2015

@author: Valentin
"""

import cv2
import numpy as np
import libardrone.libardrone as libardrone
import threading
import time

import logic
import pid


#Globale Variable für die Drone
drone = None

#True, wenn die Drone gerade eine Linie sieht. Sonst False
has_line = False

#True, wenn die Webcam als Bildquelle dienen soll. False, wenn die Drone verwendet wird
uses_webcam = True

#Webcam
cap = cv2.VideoCapture(0)

def get_picture():
    global uses_webcam
    global cal
    global drone
    if uses_webcam:
        ret, frame = cap.read()
        return frame
    return drone.get_image()
    
#Aktion ausgeben
def webcam_action(action):
    print "Doing", action

#Switch für Dronenkommandos
def drone_action(action):
    global drone
    if action == "w":
        drone.move_forward()
    elif action == "a":
        drone.move_left()
    elif action == "s":
        drone.move_backward()
    elif action == "d":
        drone.move_right()
    elif action == "q":
        drone.move_up()
    elif action == "e":
        drone.move_down()
    elif action == "l":
        drone.land()
    elif action == "h":
        drone.hover()
    elif action == "j":
        drone.turn_left()
    elif action == "k":
        drone.turn_right()
    
#Eine Aktion durchführen. Je nach Umgebung wird die Aktion ausgegeben oder ausgeführt
def do_action(action):
    global drone
    global uses_webcam
    if uses_webcam:
        webcam_action(action)
    else:
        drone_action(action)
    
def flip_direction(dir):
    

#Drone initialisieren und starten
def init():
    global drone
    
    drone = libardrone.ARDrone(1, 0) #don't need HD video
    drone.set_camera_view(0)
    drone-set_speed(0.4)
    
    drone.takeoff()
    time.sleep(2)
    
#Drone im Zickzack fliegen lassen, bis eine Linie gefunden wird
def find_line():
    global has_line
    global drone
    stop = time.time() + 10
    direction = "r"
    do_action("r")    
    
    while time.time() < stop:
        
        
def end_session():
    global drone
    drone.land()
    time.sleep(2)
    drone.halt()
        