# -*- coding: utf-8 -*-
"""
Created on Tue Aug 04 15:05:50 2015

@author: Valentin
"""



import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
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


    #if k == ord('a'):
    #    print 'capturing!'
    #    cv.SaveImage("test.jpg",frame) 