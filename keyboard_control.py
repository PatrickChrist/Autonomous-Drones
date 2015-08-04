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
        pass

    def manual_controlled(self):
        return self.manual_control