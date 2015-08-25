# -*- coding: utf-8 -*-
"""
Created on Thu Aug 06 13:31:34 2015

@author: Anne1
"""

import cv2
#import numpy as np

def draw_information (frame, centroid, left, right, up, down, forward, backward):                            #// creates just the header parts
    frame = cv2.imread("D:\Alles\Bilder\design fair\MPD Design Fair 2014 ST 133 - Kopie.jpg"); #// here we'll know the method used (allocate matrix)
    height, width = frame.shape[:2]
    cv2.circle(frame,((centroid[0]),(centroid[1])),3, (0,0,255), 2)
    cv2.circle(frame,((width/2),(height/2)), 10, (0,0,0), 2)
    cv2.line(frame,((centroid[0]),(centroid[1])),((width/2),(height/2)),(0,0,255)) 
    if left:      
        cv2.line(frame, ((width/5)-30,(height/2)-30), ((width/5)-30,(height/2)+30), (0,255,255),2)
        cv2.line(frame, ((width/8)-30,(height/2)), ((width/5)-30,(height/2)+30), (0,255,255),2)
        cv2.line(frame, ((width/8)-30,(height/2)), ((width/5)-30,(height/2)-30), (0,255,255),2)
        
    if right:
        cv2.line(frame, ((width*4/5)+30,(height/2)-30), ((width*4/5)+30,(height/2)+30), (0,255,255),2)
        cv2.line(frame, ((width*7/8)+30,(height/2)), ((width*4/5)+30,(height/2)+30), (0,255,255),2)
        cv2.line(frame, ((width*7/8)+30,(height/2)), ((width*4/5)+30,(height/2)-30), (0,255,255),2)
        
        
        #cv2.rectangle(frame,((width*7/8)-30,(height/2)-30),((width*7/8)+30,(height/2)+30),(0,255,255),2)
    if up:
        cv2.line(frame, ((width/2)-30,(height/5)), ((width/2)+30,(height/5)), (0,255,255),2)
        cv2.line(frame, ((width/2),(height/8)-20), ((width/2)+30,(height/5)), (0,255,255),2)
        cv2.line(frame, ((width/2)-30,(height/5)), ((width/2),(height/8)-20), (0,255,255),2)
        
#        cv2.rectangle(frame,((width/2)+30,(height/8)+30),((width/2)-30,(height/8)-30),(0,255,255),2)
    if down:
        cv2.line(frame, ((width/2)-30,(height*4/5)), ((width/2)+30,(height*4/5)), (0,255,255),2)
        cv2.line(frame, ((width/2),(height*7/8)+20), ((width/2)+30,(height*4/5)), (0,255,255),2)
        cv2.line(frame, ((width/2)-30,(height*4/5)), ((width/2),(height*7/8)+20), (0,255,255),2)
        
        #cv2.rectangle(frame,((width/2)-30,(height*7/8)-30),((width/2)+30,(height*7/8)+30),(0,255,255),2)
    if forward:
       cv2.rectangle(frame,((width/2)+30,(height/2)+30),((width/2)-30,(height/2)-30),(0,255,0),2) 
    if backward:
       cv2.rectangle(frame,((width/2)+30,(height/2)+30),((width/2)-30,(height/2)-30),(0,0,255),2) 
        
    cv2.imshow ("dasdassa",frame)
    cv2.waitKey (0)
              
    cv2.destroyAllWindows()
    return frame


#def get_centroid_error(centroid, width, height):
#    errx = 
#    erry = 
#    return errx, erry
#def get_centroid_error(centroid, width, height):
    
       
draw_information(0,[200, 10],True,True,True,True,True,0)
#errx, erry = cv2.circle(frame,((width/3),(height/3)),3, (0,0,255), 2)
#print erry, errx


    
#errx, erry = get_centroid_error(centroid, width, height)
#print erry, errx

#    
#def get_centroid_from_corners(npcorners):
#    return np.sum(npcorners,0) / float(len(npcorners))
#
#def get_corners_from_marker(frame):
#    corners = None
#    found, corners = cv2.A (frame)
#    npcorners = np.array(corners)
#    return found, npcorners
#

#    
##def get_distance_error(outer_corners):
#  #  short_1 = np.linalg.norm(outer_corners[0]-outer_corners[1])
#  #  short_2 = np.linalg.norm(outer_corners[3]-outer_corners[2])
#  #  long_1 = np.linalg.norm(outer_corners[1]-outer_corners[3])
#   # long_2 = np.linalg.norm(outer_corners[2]-outer_corners[0])
#    
#   # avg_short = (short_1+short_2)/2.0
#   # avg_long = (long_1+long_2)/2.0
#    
#   # dif_short = (avg_short - distance_best[0])/distance_best[0]
#   # dif_long = (avg_long - distance_best[1])/distance_best[1]
#    
#   # return (dif_short+dif_long)/2.0
#    
#    #############################################################  
#    
#running = True
#while running:    # get current image  
#    running, frame = cv2.imread() 
#   # running = manual_control(drone, running)
#        
#                height, width = frame.shape[:2]
#                errx, erry = get_centroid_error(centroid, width, height)
#                print erry, errx
#                
#           #     errdif = get_distance_error(o_corners)
##                if errx > 0:
##                    drone.move(0.0, 0.0, 0.0, 0.1)     
##                else:
##                    drone.move(0.0, 0.0, 0.0, -0.1) 
#          #  if errdif > 0:
#               # drone.move(0.0, -0.1, 0.0, 0.0)     
#          #  else:
#           #     drone.move(0.0, 0.1, 0.0, 0.0) 
#                    
#                #draw inner circle
#            #    cv2.circle(frame, (centroid[0][0],centroid[0][1]), 10,(255,0,0) ,1)
#            #    cv2.line(frame, (o_corners[0][0],o_corners[0][1]), (o_corners[1][0],o_corners[1][1]), (0,255,0),1)
#             #   cv2.line(frame, (o_corners[1][0],o_corners[1][1]), (o_corners[3][0],o_corners[3][1]), (0,255,255),1)
#             #   cv2.line(frame, (o_corners[3][0],o_corners[3][1]), (o_corners[2][0],o_corners[2][1]), (0,0,255),1)
#           #     cv2.line(frame, (o_corners[2][0],o_corners[2][1]), (o_corners[0][0],o_corners[0][1]), (255,255,0),1)
#            #    get_distance_error(o_corners)
#           # if not found:
#          #      print 'chessboard not found'
#            #    drone.hover()
#            #    continue
#            
#       #     cv2.imshow('frame', frame)  