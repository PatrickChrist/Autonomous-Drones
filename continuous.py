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
    


    

#Drone initialisieren und starten
def init_session():
    global drone
    
    drone = libardrone.ARDrone(1, 0) #don't need HD video
    drone.set_camera_view(0)
    drone.set_speed(0.4)
    
    drone.takeoff()
    time.sleep(2)
    
#Drone im Zickzack fliegen lassen, bis eine Linie gefunden wird
def find_line():
    global has_line
    global drone
    pid.movement(drone)
    time.sleep(5)
    drone.hover()
    
def follow_line():
    global has_line
    global drone
    if has_line:
        print "following"
    else:
        find_line()
        
#Landet und wartet. Zuletzt wird die Verbindung getrennt (und der Port freigegeben)
def end_session():
    global drone
    drone.land()
    time.sleep(4)
    drone.halt()
        