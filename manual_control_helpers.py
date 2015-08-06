# -*- coding: utf-8 -*-
"""
Created on Tue Aug 04 21:11:26 2015

@author: Valentin
"""

import cv2
import time
import libardrone.libardrone as libardrone


action_duration = 0.5

def make_drone():
    drone = libardrone.ARDrone(1, 1)
    drone.set_camera_view(0)
    return drone


def test_config():
	global drone
	print drone

def show_img(img):
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# one function to move them all
def drone_move(action, iterations=1):
    global drone
    global action_duration
    drone.action
    if iterations > 0:
    	time.sleep(action_duration * iterations)
    	drone.hover()

def right(i=1):
    a = move_right()
    drone_move(a, i)
    
def left(i=1):
    a = move_left()
    drone_move(a, i)
    
def tright(i=1):
    a = turn_right()
    drone_move(a, i)
    
def tleft():
    a = turn_left(i=1)
    drone_move(a, i)
    
def up(i=1):
    a = move_up()
    drone_move(a, i)
    
def down(i=1):
    a = move_down()
    drone_move(a, i)
    
def back(i=1):
    a = move_backwards()
    drone_move(a, i)
  
def go(i=1):
    a = move_forward()
    drone_move(a, i)
    
def hover():
    a = hover()
    drone_move(a)

def takeoff():
    a = takeoff()
    drone_move(a)

def land():
    global drone
    drone.land()

def speed(s):
    global drone
    drone.set_speed(s)
    
def img():
    global drone
    show_img(drone.get_image())

def navdata():
    global drone
    print drone.navdata[0]
    
def xoxo():
    global drone
    drone.halt()

def move(x, z, y, r):
    """ die eierlegende Wollmilchsau
    x: left [-1..1] right
    z: go [-1..1] back
    y: down [-1..1] up
    r: left [-1..1] right (rotation)
    """
    global drone
    drone.move(x, z, y, r)

def fly():
    foto = cv2.imread('img/wasd.jpg')
    cv2.imshow('Drone', foto) # show the frame

    ## key test
    print 'läuft'
    fly = True
    #TODO open a new window, else keys won't work
    while(fly):
        k = cv2.waitKey(33)
        
        if k == -1:
            hover(0) # do nothing
            
        # wasd for front/back/left/right
        if k == ord('a'):
            left(0)
        elif k == ord('d'):
            right(0)
        elif k == ord('w'):
            go(0)
        elif k == ord('s'):
            back(0)
            
        # arrow keys for up/down/rotate
        elif k == 63232:
            up(0)
        elif k == 63233:
            down(0)
        elif k == 63234:
            tleft(0)
        elif k == 63235:
            tright(0)
            
        # space bar makes the drone hover
        elif k == 32:
            hover(0)
        # l to land
        elif k == ord('l'):
            land(0)
        # t for takeoff
        elif k == ord('k'):
            takeoff(0)
        # n gets navdata
        elif k == ord('n'):
            navdata(0)
    
        # killall
        elif k == 27:
            fly = False
            cv2.destroyAllWindows()
        
#        if k != -1:
#            print 'key pressed:', k # else print its 
    