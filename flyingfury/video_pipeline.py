__author__ = 'Benedikt'

import threading
import autonomous_flight
import cv2


class Pipeline(threading.Thread):
    def __init__(self, drone, interface):
        super(Pipeline, self).__init__()
        self.drone = drone
        self.interface = interface
        self.cv_win = "Fury"
        self.af = autonomous_flight.AF(0, self.cv_win, self.drone, interface)

    def stop(self):
        self.af.stop()

    def run(self):
        self.af.run()
        # to steer: interface.steer_autonomous("up")
        
        
if __name__ == '__main__':
    import libardrone.libardrone as libardrone
    print "video_pipeline main"
    Pipeline(libardrone.ARDrone(1,1)).run()
