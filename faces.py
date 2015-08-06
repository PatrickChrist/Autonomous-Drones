# -*- coding: utf-8 -*-
"""
Created on Wed Aug 05 17:18:05 2015

@author: Valentin
"""

import numpy as np
import cv2
import libardrone.libardrone as libardrone
import threading
import time


faceCascade = cv2.CascadeClassifier('C:\opencv\data\haarcascades\haarcascade_frontalface_default.xml')

def detect_faces(frame, b):
    global face
    print "finding faces"
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(60, 60)
    )

    # Draw a rectangle around the faces
    if len(faces) > 0:
        print "found face"
        face = faces[0]

drone = libardrone.ARDrone(1, 0)
drone.set_camera_view(1)


face = None
iteration = 0

running = True
while running:
    
#    time.sleep(0.5)

    frame = drone.get_image()
    
    iteration = iteration + 1
    #print iteration
    if iteration > 20:
        iteration = 0
        
        thread = threading.Thread(target=detect_faces, args=(frame, "thread"))
        thread.start()
    
    
        
    if face != None:
        (x, y, w, h) = face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#video_capture.release()
cv2.destroyAllWindows()


