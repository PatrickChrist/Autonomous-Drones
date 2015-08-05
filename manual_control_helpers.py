# -*- coding: utf-8 -*-
"""
Created on Tue Aug 04 21:11:26 2015

@author: Valentin
"""

import cv2
import time

action_duration = 0.5

def show_img(img):
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# eine
def drone_move(action, iterations=1):
    global drone
    global action_duration
    while iterations >0:
        drone.action
        time.sleep(action_duration)
    drone.hover()

def right(i=1):
    a = drone.move_right()
    drone_move(a, i)
    
def left(i=1):
    a = drone.move_left()
    drone_move(a, i)
    
def tright(i=1):
    a = drone.turn_right()
    drone_move(a, i)
    
def tleft():
    a = drone.turn_left(i=1)
    drone_move(a, i)
    
def up(i=1):
    a = drone.move_up()
    drone_move(a, i)
    
def down(i=1):
    a = drone.move_down()
    drone_move(a, i)
    
def back(i=1):
    a = drone.move_backwards()
    drone_move(a, i)
  
def go(i=1):
    a = drone.move_forward()
    drone_move(a, i)
    
def land():
    a = drone.land()
    drone_move(a)
    
def hover():
    a = drone.hover()
    drone_move(a)

def takeoff():
    a = drone.takeoff()
    drone_move(a)
    
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
        
#        if k == -1:
#            k = k # do nothing
            
        # wasd for front/back/left/right
        if k == ord('a'):
            left()
        elif k == ord('d'):
            right()
        elif k == ord('w'):
            go()
        elif k == ord('s'):
            back()
            
        # arrow keys for up/down/rotate
        elif k == 63232:
            up()
        elif k == 63233:
            down()
        elif k == 63234:
            tleft()
        elif k == 63235:
            tright()
            
        # space bar makes the drone hover
        elif k == 32:
            hover()
        # l to land
        elif k == ord('l'):
            land()
        # t for takeoff
        elif k == ord('k'):
            takeoff()
        # n gets navdata
        elif k == ord('n'):
            navdata()
    
        # killall
        elif k == 27:
            fly = False
            cv2.destroyAllWindows()
        
#        if k != -1:
#            print 'key pressed:', k # else print its 
    