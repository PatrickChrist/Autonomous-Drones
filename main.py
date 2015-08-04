__author__ = 'Benedikt'

from libardrone import libardrone
import cv2
import numpy
import keyboard_control
import video_pipeline


class Tower:
    def __init__(self, drone):
        self.drone = drone
        self.manual_steering = False

    def steer(self, command):
        pass  # TODO

    def steer_autonomous(self, command):
        if self.manual_steering:
            print "disregarding input while in manual mode"
            return
        self.steer(command)


def main_loop():
    running = True
    while running:
        key = cv2.waitKey(33)
        keyboard.on_key(key)


def init():
    drone.reset()


drone = libardrone.ARDrone(True, True)
interface = Tower(drone)


if __name__ == '__main__':
    keyboard = keyboard_control.KeyboardControl(drone)
    pipeline = video_pipeline.Pipeline(drone)
    cv2.imshow('Drone', numpy.zeros((10, 10)))

    try:
        init()
        main_loop()
    except Exception, e:
        print "Going down.", e
        drone.land()
    finally:
        drone.halt()
        cv2.destroyAllWindows()
