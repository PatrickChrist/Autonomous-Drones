__author__ = 'Benedikt'

import cv2

class Pipeline:
    def __init__(self, drone):
        self.drone = drone
        self.cv_win = "Fury"

    def on_frame(self):
        # will be called roughly every 33ms
        image = self.drone.get_image()
        # ...
        cv2.imshow(self.cv_win, ...)