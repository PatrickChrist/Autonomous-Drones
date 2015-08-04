__author__ = 'Benedikt'

from libardrone import libardrone
import cv2
import numpy


def fly():
    drone.reset()
    running = True
    return_to_hover = False
    flying = False
    while running:
        key = cv2.waitKey(33)
        if key == 27:  # esc
            if flying:
                drone.land()
            running = False
            continue
        if key == ord('p'):
            drone.reset()
            continue

        if not flying:
            if key == ord(' '):
                drone.takeoff()
                drone.hover()
                flying = True
        else:
            if key == ord(' '):
                drone.hover()
                drone.land()
                flying = False
            elif key == ord('w'):
                return_to_hover = True
                drone.move_forward()
            elif key == ord('a'):
                return_to_hover = True
                drone.move_left()
            elif key == ord('s'):
                return_to_hover = True
                drone.move_backward()
            elif key == ord('d'):
                return_to_hover = True
                drone.move_right()
            elif key == ord('q'):
                return_to_hover = True
                drone.turn_left()
            elif key == ord('e'):
                return_to_hover = True
                drone.turn_right()
            elif key == 2490368:  # up
                return_to_hover = True
                drone.move_up()
            elif key == 2621440:  # down
                return_to_hover = True
                drone.move_down()
            elif key == ord('1'):
                drone.speed = 0.1
            elif key == ord('2'):
                drone.speed = 0.3
            elif key == ord('3'):
                drone.speed = 0.5
            elif key == ord('4'):
                drone.speed = 0.9
            else:
                if return_to_hover:
                    return_to_hover = False
                    drone.hover()

        show_frame()


def show_frame():
    try:
        pixelarray = drone.get_image()  # get an frame form the Drone
        frame = pixelarray[:, :, ::-1].copy()  # convert to a frame
        cv2.imshow('Drone', frame)
    except Exception, ex:
        print "Image showing failed", ex


if __name__ == '__main__':
    drone = libardrone.ARDrone(True, True)
    cv2.imshow('Drone', numpy.zeros((10, 10)))

    try:
        fly()
    except Exception, e:
        print "Going down.", e
        drone.land()
    finally:
        drone.halt()
        cv2.destroyAllWindows()
