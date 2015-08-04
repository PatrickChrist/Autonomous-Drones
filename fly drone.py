# -*- coding: utf-8 -*-

import libardrone.libardrone as libardrone #import the libardrone 


d=libardrone.ARDrone(1,1) #initalize the Drone Object


"""
    CONTROLS:
        
    d.takeoff()
    d.hover()
    
    d.land()
    d.halt()
    
    d.move_up()
    d.move_down()
    
    d.move_forward()
    d.move_backward()
    
    d.move_right()
    d.move_left()
    
    d.set_speed() # 0.0 - 1.0
    
    
    VALUES:
    
    d.get_navdata()
                values = dict(zip(['ctrl_state', 'battery', 'theta', 'phi', 'psi', 'altitude', 'vx', 'vy', 'vz', 'num_frames'], values))
    
    n['altitude']
    
    
"""
def data():    
    navdata = d.get_navdata()
    n= navdata[0]
    alt = n['altitude']
    
#print 'altitude: ' + n['altitude']
#print 'vx: ' + n['vx'] + ' vy: ' + n['vy'] + ' vz: ' + n['vz']

