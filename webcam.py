# -*- coding: utf-8 -*-
"""
Created on Tue Aug 04 15:05:50 2015

@author: Valentin
"""



import numpy as np
import cv2
import math

cap = cv2.VideoCapture(0)

def middle(start, end, a, b):
    x0, y0 = start
    xn, yn = end
    print start
    print end
    print a
    print b
    in_range = None
    num_in_range = 0
    while x0 < xn and y0 < yn:
        x0 -= b
        y0 += a
        if x0 >= 0 and y0 >= 0 and x0 <= 320 and y0 <= 180:
            if in_range == None:
                in_range = (x0, y0)
            num_in_range += 1
    if in_range != None:
        xl, yl = in_range
        return (xl + (-b) * (num_in_range / 2), yl + a * (num_in_range / 2))
    return (0, 0)
            
def middle(start, end, a, b):
    x0, y0 = start
    xn, yn = end
    print start
    print end
    print a
    print b
    in_range = None
    out_range = None
    num_in_range = 0
    while x0 < xn and y0 < yn:
        x0 -= b
        y0 += a
        if x0 >= 0 and y0 >= 0 and x0 <= 320 and y0 <= 180:
            if in_range == None:
                in_range = (x0, y0)
            num_in_range += 1
            out_range = (x0, y0)
    if in_range != None:
        xl, yl = in_range
        return (xl + (-b) * (num_in_range / 2), yl + a * (num_in_range / 2))
    return (0, 0)


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    
    resized = cv2.resize(frame, (320, 180)) #resize image
    # display the image
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
    #convert colors
    gray = cv2.cvtColor(blur, cv2.COLOR_HSV2BGR)
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(blur,50,150,apertureSize = 3) 
    #find lines
    lines = cv2.HoughLines(edges,1,np.pi/180,50)
    if lines is not None:
            
        for rho,theta in lines[0]:
            a = abs(np.cos(theta))
            b = np.sin(theta)
            
            
            x = a * rho
            y = b * rho
            
            x, y = middle((x - 1000 * b, y + 1000 * a), (x + 1000 * b, y - 1000 * a), a, b)
            print x
            
            if theta < math.pi / 2:
                b = -b
                
            w, h, d = frame.shape
            
            cv2.line(frame, (int(w/2), int(h/2)), (int(w/2+b*1000), int(h/2-a*1000)), (255, 0, 255))
            cv2.line(edges, (int(x), int(0)), (int(x), 1000), (255, 255, 255))
            lr = str(b / 3)
            rb = str(-a / 3)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame,'lr: ' + lr,(10,70), font, 1,(255,255,255),2)
            cv2.putText(frame,'rb: ' + rb,(10,120), font, 1,(255,255,255),2)
            
    
    
    cv2.imshow('frame',edges)
    
    k = cv2.waitKey(1)
    
    if k == ord('q'):
        break
    

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


    #if k == ord('a'):
    #    print 'capturing!'
    #    cv.SaveImage("test.jpg",frame) 