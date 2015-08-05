# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 23:22:51 2015

@author: dadrian
"""

import time, sys
import ps_drone                                              # Import PS-Drone
import cv2
import numpy as np

# FUCKING GLOBALS YEE
pattern_size = (4, 5)
distance_best = [55, 75]

##FLIGHT MODE###

class PID:
    
    def __init__(self, Kp=0.25, Kd=0.25, Ki=0.05):
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki
        self.last_err_x = 0
        self.last_err_y = 0 
    
    def action(self, err_x, err_y):
        out_x = self.Kp*err_x + self.Ki*(err_x+self.last_err_x) + self.Kd*(err_x-self.last_err_x)
        out_y = self.Kp*err_y + self.Ki*(err_y+self.last_err_y) + self.Kd*(err_y-self.last_err_y)
        self.last_err_x = err_x
        self.last_err_y = err_y
        return out_x, out_y
    
def get_main_corners_from_corners(npcorners):
    return np.array([npcorners[0][0],npcorners[3][0],npcorners[16][0],npcorners[19][0]])
    
def get_centroid_from_corners(npcorners):
    return np.sum(npcorners,0) / float(len(npcorners))

def get_corners_from_marker(frame):
    corners = None
    found, corners = cv2.findChessboardCorners(frame, pattern_size, corners, cv2.CALIB_CB_FAST_CHECK)
    npcorners = np.array(corners)
    return found, npcorners

def get_centroid_error(centroid, width, height):
    errx = (centroid[0][0] - width/2.0)/(width/2.0)
    erry = (centroid[0][1] - height/2.0)/(height/2.0)
    return errx, erry
    
def get_distance_error(outer_corners):
    short_1 = np.linalg.norm(outer_corners[0]-outer_corners[1])
    short_2 = np.linalg.norm(outer_corners[3]-outer_corners[2])
    long_1 = np.linalg.norm(outer_corners[1]-outer_corners[3])
    long_2 = np.linalg.norm(outer_corners[2]-outer_corners[0])
    
    avg_short = (short_1+short_2)/2.0
    avg_long = (long_1+long_2)/2.0
    
    dif_short = (avg_short - distance_best[0])/distance_best[0]
    dif_long = (avg_long - distance_best[1])/distance_best[1]
    
    return (dif_short+dif_long)/2.0

def start_up_drone():
    drone = ps_drone.Drone()								# Start using drone
    
    drone.startup()									# Connects to drone and starts subprocesses
    drone.reset()										# Always good, at start
    
    while drone.getBattery()[0] == -1:	time.sleep(0.1)		      # Waits until the drone has done its reset
    time.sleep(0.5)									# Give it some time to fully awake
    
    drone.printBlue("Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1]))	# Gives a battery-status
    return drone
    
def main():
    drone = start_up_drone()
    drone.sdVideo()             
    drone.videoFPS(30)                      
    drone.frontCam()                                             # Choose front view

    drone.trim()
    cam = cv2.VideoCapture('tcp://192.168.1.1:5555')
    
    #cam = cv2.VideoCapture(0)
    pid = PID(0.5,1.0,0.15)
    print "Created VideoCapture"
    
#    #debug video boot sequence
#    count = 0
#    while count < 20*30:    # get current frame of video    
#        running, frame = cam.read()    
#        if running:
#            cv2.imshow('frame', frame)  
#            count += 1
#    
    running = True
    while running:    # get current frame of video   
        running, frame = cam.read()      
        
        ######################################
        # Controll Drone with Keyboard section
        key = drone.getKey()
        if key == " ":
            if drone.NavData["demo"][0][2] and not drone.NavData["demo"][0][3]:	drone.takeoff()
            else:	drone.land()
        elif key != "":	
            running = False
            drone.land()
            break
        ######################################
        
        if running:    
            found, corners = get_corners_from_marker(frame)
            if found:
                centroid = get_centroid_from_corners(corners)
                o_corners = get_main_corners_from_corners(corners)
                height, width = frame.shape[:2]
                errx, erry = get_centroid_error(centroid, width, height)
                out_x,out_y = pid.action(errx,erry)
                print erry, out_y
                
                errdif = get_distance_error(o_corners)
#                if errx > 0:
#                    drone.move(0.0, 0.0, 0.0, 0.1)     
#                else:
#                    drone.move(0.0, 0.0, 0.0, -0.1) 
                if errdif > 0:
                    drone.move(0.0, -0.1, 0.0, 0.0)     
                else:
                    drone.move(0.0, 0.1, 0.0, 0.0) 
                    
                #draw inner circle
                cv2.circle(frame, (centroid[0][0],centroid[0][1]), 10,(255,0,0) ,1)
                cv2.line(frame, (o_corners[0][0],o_corners[0][1]), (o_corners[1][0],o_corners[1][1]), (0,255,0),1)
                cv2.line(frame, (o_corners[1][0],o_corners[1][1]), (o_corners[3][0],o_corners[3][1]), (0,255,255),1)
                cv2.line(frame, (o_corners[3][0],o_corners[3][1]), (o_corners[2][0],o_corners[2][1]), (0,0,255),1)
                cv2.line(frame, (o_corners[2][0],o_corners[2][1]), (o_corners[0][0],o_corners[0][1]), (255,255,0),1)
                get_distance_error(o_corners)
            if not found:
                print 'chessboard not found'
                drone.hover()
                continue
            
            cv2.imshow('frame', frame)  
          
            if cv2.waitKey(1) & 0xFF == 27:             # escape key pressed            
                running = False    
            else:        # error reading frame        
    		print 'error reading video feed'
      
    cam.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()