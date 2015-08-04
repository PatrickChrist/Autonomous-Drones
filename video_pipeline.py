__author__ = 'Benedikt'

import cv2
import autonomous_flight

class Pipeline:
    def __init__(self, drone):
        self.drone = drone
        self.cv_win = "Fury"

    def on_frame(self):
        af = autonomous_flight.AF(0,self.cv_win,self.drone)
        af.run()
        
        
if __name__ == '__main__':
    import libardrone.libardrone as libardrone
    
    Pipeline(libardrone.ARDrone(1,1)).on_frame()
