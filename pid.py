# -*- coding: utf-8 -*-
"""
Created on Thu Aug 06 13:01:24 2015

@author: Valentin
"""

import libardrone.libardrone as libardrone

vx = 0
vy = 0
vz = 0
altitude = 0
phi = 0
psi = 0
theta = 0

tar_x = 0
tar_y = 0
tar_phi = 0

K = 0.15

def sense(drone):
    global vx
    global vy
    global vz
    global altitude
    global phi
    global psi
    global theta
    tmp = drone.navdata
    vx = tmp['vx']
    vy = tmp['vy']
    vz = tmp['vz']
    altitude = tmp['altitude']
    phi = tmp['phi']
    psi = tmp['psi']
    theta = tmp['theta']
    return (vx, vy, vz, altitude, phi, psi, theta)
    

def right(speed):
    global tar_x
    tar_x = speed
    
def left(speed):
    global tar_x
    tar_x = -speed
    
def forward(speed):
    global tar_y
    tar_y = -speed
    
def backward(speed):
    global tar_y
    tar_y = speed
    

def movement(drone):
    global tar_x
    global tar_y
    global vx
    global vy
    
    dx = tar_x - vx
    dy = tar_y - vy
        
    
    #drone.at(drone.at_pcmd, True, K*(dx), K*(dy), 0, 0);
    print drone.navdata
    
