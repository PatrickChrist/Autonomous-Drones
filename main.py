import time

__author__ = 'Benedikt'

from libardrone import libardrone
import cv2
import numpy
import keyboard_control
import video_pipeline


class Tower:  # controls the drone movements
    def __init__(self, drone):
        self.drone = drone
        self.manual_steering = False
        self.flying = False

    def set_manual_mode(self, value):
        self.manual_steering = value

    def steer(self, command, speed=0.3):
        self.drone.speed = speed
        if command == "up":
            self.drone.move_up()
        if command == "down":
            self.drone.move_down()
        if command == "left":
            self.drone.move_left()
        if command == "right":
            self.drone.move_right()
        if command == "turnleft":
            self.drone.turn_left()
        if command == "turnright":
            self.drone.turn_right()
        if command == "forward":
            self.drone.move_forward()
        if command == "backward":
            self.drone.move_backward()
        if command == "takeoff":
            if self.flying:
                return
            else:
                self.flying = True
                self.drone.takeoff()
        if command == "land":
            if self.flying:
                self.flying = False
                self.drone.land()
            else:
                return
        if command == "reset":
            self.flying = False
            self.drone.reset()
        if command == "hover":
            self.drone.hover()
        if command == "toggle_flying":
            if self.flying:
                self.drone.land()
            else:
                self.drone.takeoff()
            self.flying = not self.flying

    def steer_manual(self, command, speed=0.3):
        self.set_manual_mode(True)
        self.steer(command, speed)

    def steer_autonomous(self, command, speed=0.3):
        if self.manual_steering:
            print "disregarding input while in manual mode"
        else:
            self.steer(command, speed)


def main_loop():
    running = True
    while running:
        key = cv2.waitKey(33)
        running = keyboard.on_key(key)


def init():
    drone.reset()

print "setting up drone..."
drone = libardrone.ARDrone(True, False)
global interface
interface = Tower(drone)
print "starting up!"

if __name__ == '__main__':
    keyboard = keyboard_control.KeyboardControl(drone, interface)
    pipeline = video_pipeline.Pipeline(drone, interface)
    pipeline.daemon = True
    cv2.imshow('Fury', numpy.zeros((10, 10)))

    try:
        init()
        pipeline.start()
        main_loop()
    except Exception, e:
        print "Going down.", e
        drone.land()
    finally:
        drone.halt()
        pipeline.stop()
        time.sleep(1)
        cv2.destroyAllWindows()
