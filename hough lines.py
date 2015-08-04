# -*- coding: utf-8 -*-

#import libardrone.libardrone as libardrone #import the libardrone 
import cv2 #import opencv
import numpy as np
import matplotlib as matplot


#load image
img = cv2.imread('img.png', 1)
#convert to HSV
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
#color ranges for red
#from 0 to 20
first_lower_red = np.array([0,50,50])
first_upper_red = np.array([20,255,255])
#from 160 to 180
second_lower_red = np.array([160,50,50])
second_upper_red = np.array([180,255,255])
#make a mask from those 2 thresholds
mask1 = cv2.inRange(hsv, first_lower_red, first_upper_red)
mask2 = cv2.inRange(hsv, second_lower_red, second_upper_red)
mask = cv2.add(mask1, mask2)

#put that mask on the pic
res = cv2.bitwise_and(hsv, hsv, mask= mask)




#######

gray = cv2.cvtColor(hsv,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,100,250,apertureSize = 3)

cv2.imshow('canny',edges)
cv2.waitkey(0)
#
#lines = cv2.HoughLines(edges,1,np.pi/180,200)
#for rho,theta in lines[0]:
#    a = np.cos(theta)
#    b = np.sin(theta)
#    x0 = a*rho
#    y0 = b*rho
#    x1 = int(x0 + 1000*(-b))
#    y1 = int(y0 + 1000*(a))
#    x2 = int(x0 - 1000*(-b))
#    y2 = int(y0 - 1000*(a))
#
#    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
#
#cv2.imwrite('houghlines3.jpg',img)