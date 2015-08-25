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
distance_best = [75, 95]

##FLIGHT MODE###

class PID:
    
    def __init__(self, Kp=0.25, Kd=0.25, Ki=0.05):
        self.Kp = Kp
        self.Kd = Kd
        self.Ki = Ki
        self.last_err = 0
    
    def action(self, err):
        out = self.Kp*err + self.Ki*(err+self.last_err) + self.Kd*(err-self.last_err)
        self.last_err = err
        return out
    
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
    
    drone.useDemoMode(True)
    
    while drone.getBattery()[0] == -1:	time.sleep(0.1)		      # Waits until the drone has done its reset
    time.sleep(0.5)									# Give it some time to fully awake
    
    drone.printBlue("Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1]))	# Gives a battery-status
    return drone

def manual_control (drone, running):
    running_internal = running
    key = drone.getKey()    
    if key == " ":
        if drone.NavData["demo"][0][2] and not drone.NavData["demo"][0][3]:	drone.takeoff()
        else: drone.land()															
    elif key == "0":	drone.hover()
    elif key == "w":	drone.moveForward()
    elif key == "s":	drone.moveBackward()
    elif key == "a":	drone.moveLeft()
    elif key == "d":	drone.moveRight()
    elif key == "q":	drone.turnLeft()
    elif key == "e":	drone.turnRight()
    elif key == "7":	drone.turnAngle(-10,1)
    elif key == "9":	drone.turnAngle( 10,1)
    elif key == "4":	drone.turnAngle(-45,1)
    elif key == "6":	drone.turnAngle( 45,1)
    elif key == "1":	drone.turnAngle(-90,1)
    elif key == "3":	drone.turnAngle( 90,1)
    elif key == "8":	drone.moveUp()
    elif key == "2":	drone.moveDown()
    elif key != "":
        running_internal = False
        drone.land()
        #return key
    return running_internal

def flush_capture_stream(cam):
    delay = 0
    t0 = 0
    t1 = 0
    #print doing flush
    while delay < 25:
        t0 = time.time()
        cam.read()
        t1 = time.time()
        delay = (t1 - t0) * 1000
        
def main():
    drone = start_up_drone()
    drone.sdVideo()             
    #drone.videoFPS(30)              
    drone.fastVideo()      
    drone.mp4Video()
    drone.videoBitrate(250)
    drone.frontCam()           
    CDC = drone.ConfigDataCount
    while CDC==drone.ConfigDataCount: time.sleep(0.001)
    drone.startVideo()

    drone.trim()
    #cam = cv2.VideoCapture('tcp://192.168.1.1:5555')
    
    #cam = cv2.VideoCapture(0)
    rotation_pid = PID(0.6,0.6,0.05)
    height_pid = PID(0.1,0.1,0.01)
    dist_pid = PID(0.2,0.25,0.1)

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
    IMC = drone.VideoImageCount

    while running:    # get current frame of video   
        #running, frame = cam.read() 
        running = manual_control(drone, running)

        while drone.VideoImageCount==IMC:   time.sleep(0.01)
            
        frame = drone.VideoImage
        
        if running:    
            found, corners = get_corners_from_marker(frame)
            if found:
                centroid = get_centroid_from_corners(corners)
                o_corners = get_main_corners_from_corners(corners)
                height, width = frame.shape[:2]
                errx, erry = get_centroid_error(centroid, width, height)
                errdif = get_distance_error(o_corners)
                ox = rotation_pid.action(errx)
                oy = height_pid.action(erry)
                odist = dist_pid.action(errdif)
                
                print ox, oy, odist
                drone.move(0.0,-float(odist),-float(oy),float(ox))
                    
                cv2.circle(frame, (centroid[0][0],centroid[0][1]), 10,(255,0,0) ,1)
                cv2.line(frame, (o_corners[0][0],o_corners[0][1]), (o_corners[1][0],o_corners[1][1]), (0,255,0),1)
                cv2.line(frame, (o_corners[1][0],o_corners[1][1]), (o_corners[3][0],o_corners[3][1]), (0,255,255),1)
                cv2.line(frame, (o_corners[3][0],o_corners[3][1]), (o_corners[2][0],o_corners[2][1]), (0,0,255),1)
                cv2.line(frame, (o_corners[2][0],o_corners[2][1]), (o_corners[0][0],o_corners[0][1]), (255,255,0),1)
                get_distance_error(o_corners)
            if not found:
                print 'chessboard not found'
                drone.hover()
                #do_flush = True
                continue
            
            cv2.imshow('frame', frame)  
          
            if cv2.waitKey(1) & 0xFF == 27:             # escape key pressed            
                running = False    
            else:        # error reading frame        
                print 'error reading video feed'
        else:
            drone.hover() # got no frame update, better hover for now
            
    #,cam.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()