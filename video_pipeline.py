__author__ = 'Benedikt'

import threading
import autonomous_flight
import cv2
from main import interface


class Pipeline(threading.Thread):
    def __init__(self, drone):
        super(Pipeline, self).__init__()
        self.drone = drone
        self.cv_win = "Fury"

    def run(self):
        af = autonomous_flight.AF(0, self.cv_win, self.drone)
        af.run()
        # to steer: interface.steer_autonomous("up")
        
        
if __name__ == '__main__':
    import libardrone.libardrone as libardrone
    
    Pipeline(libardrone.ARDrone(1,1)).run()
