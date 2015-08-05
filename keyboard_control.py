__author__ = 'Benedikt'


class KeyboardControl:
    def __init__(self, drone, interface):
        self.drone = drone
        self.return_to_hover = False
        self.speed = 0.3
        self.interface = interface

    """ on_key(key)
        :param key: keycode from cv2
        :returns truth value whether to continue running
    """
    def on_key(self, key):
        if key == 27:  # esc
            self.interface.steer_manual("land")
            return False

        if key == ord('p'):
            self.interface.steer_manual("reset")
        elif key == ord('t'):
            self.interface.set_manual_mode(False)
        elif key == ord(' '):
            self.interface.steer_manual('toggle_flying')
        elif key == ord('w'):
            self.return_to_hover = True
            self.interface.steer_manual("forward", speed=self.speed)
        elif key == ord('a'):
            self.return_to_hover = True
            self.interface.steer_manual("left", speed=self.speed)
        elif key == ord('s'):
            self.return_to_hover = True
            self.interface.steer_manual("backward", speed=self.speed)
        elif key == ord('d'):
            self.return_to_hover = True
            self.interface.steer_manual("right", speed=self.speed)
        elif key == ord('q'):
            self.return_to_hover = True
            self.interface.steer_manual("turnleft", speed=self.speed)
        elif key == ord('e'):
            self.return_to_hover = True
            self.interface.steer_manual("turnright", speed=self.speed)
        elif key == 2490368:  # up
            self.return_to_hover = True
            self.interface.steer_manual("up", speed=self.speed)
        elif key == 2621440:  # down
            self.return_to_hover = True
            self.interface.steer_manual("down", speed=self.speed)
        elif key == ord('1'):
            self.speed = 0.1
        elif key == ord('2'):
            self.speed = 0.3
        elif key == ord('3'):
            self.speed = 0.5
        elif key == ord('4'):
            self.speed = 0.9
        else:
            if self.return_to_hover:
                self.return_to_hover = False
                self.interface.steer_manual("hover")

        return True
