__author__ = 'Benedikt'

from main import interface

class KeyboardControl:
    def __init__(self, drone):
        self.drone = drone
        self.manual_control = False

    """ on_key(key)
        :param key: keycode from cv2
        :returns truth value whether to continue running
    """
    def on_key(self, key):
        if key == 27:  # esc
            interface.steer_manual("land")
            return False

        if key == ord('p'):
            interface.steer_manual("reset")

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

            return True

    def manual_controlled(self):
        return self.manual_control