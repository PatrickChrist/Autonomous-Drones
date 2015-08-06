# -*- coding: utf-8 -*-
import collections

import cv2 #import opencv
import video
import numpy as np
import autopilot_agent as aa
import face_tracker
import time

def tup_abs(tuple):
    return tuple([abs(i) for i in tuple])

def tuple_absolute_difference(a, b):
    return tuple([abs(x - y) for x, y in zip(a, b)])

X_LOWER = -70
X_UPPER = 70
Y_LOWER = 40
Y_UPPER = 45
Y_CENTER = (Y_UPPER + Y_LOWER) / 2
Z_LOWER = -70
Z_UPPER = 10
Z_CENTER = (Z_UPPER + Z_LOWER) / 2

class AF(object):
    def __init__(self, video_src, window_name,drone, interface):
        self.controller = Pcontroller()
        self.consequtive_misses = 0
        self.drone = drone
        self.window_name = window_name
        self.cam = video.create_capture(video_src)
        ret, self.frame = self.cam.read()
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.onmouse)

        self.selection = None
        self.drag_start = None
        self.tracking_state = 0
        self.show_backproj = False

        self.lastface = None

        self.interface = interface
        self.running = True

    def stop(self):
        self.running = False

    def onmouse(self, event, x, y, flags, param):
        x, y = np.int16([x, y]) # BUG
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drag_start = (x, y)
            self.tracking_state = 0
        if self.drag_start:
            if flags & cv2.EVENT_FLAG_LBUTTON:
                h, w = self.frame.shape[:2]
                xo, yo = self.drag_start
                x0, y0 = np.maximum(0, np.minimum([xo, yo], [x, y]))
                x1, y1 = np.minimum([w, h], np.maximum([xo, yo], [x, y]))
                self.selection = None
                if x1-x0 > 0 and y1-y0 > 0:
                    self.selection = (x0, y0, x1, y1)
            else:
                self.drag_start = None
                if self.selection is not None:
                    self.tracking_state = 1

    def show_hist(self):
        bin_count = self.hist.shape[0]
        bin_w = 24
        img = np.zeros((256, bin_count*bin_w, 3), np.uint8)
        for i in xrange(bin_count):
            h = int(self.hist[i])
            cv2.rectangle(img, (i*bin_w+2, 255), ((i+1)*bin_w-2, 255-h), (int(180.0*i/bin_count), 255, 255), -1)
        img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
        cv2.imshow('hist', img)

    def steer_to(self, right, down, size):
        facesize = (size[0] + size[1]) / 2.0
        command, speed = self.controller.adjust(right, size, down)
        self.interface.steer_autonomous(command, speed)
        # print down, facesize
        # if right < X_LOWER:
        #     self.interface.steer_autonomous("turnleft", 0.15)
        # elif right > X_UPPER:
        #     self.interface.steer_autonomous("turnright", 0.15)
        # elif down < Z_LOWER:
        #     self.interface.steer_autonomous("up", 0.4)
        # elif down > Z_UPPER:
        #     self.interface.steer_autonomous("down", 0.4)
        # elif facesize > Y_UPPER:  # too big, move away
        #     self.interface.steer_autonomous("backward", 0.05)
        # elif facesize < Y_LOWER:
        #     self.interface.steer_autonomous("forward", 0.05)
        # else:
        #     self.interface.steer_autonomous("hover")

    def run(self):
        # self.run_old()
        self.run_new()

    def run_old(self):
        while self.running:
            # This should be an numpy image array
            pixelarray = self.drone.get_image() # get an frame form the Drone
            if pixelarray is not None: # check whether the frame is not empty
                self.frame = pixelarray[:, :, ::-1].copy() #convert to a frame
#            ret, self.frame = self.cam.read()
                
            size = self.frame.shape
            act = aa.action(self.frame,size[1],size[0],0,0,0,0,0,0,0,0,0)
            c = (int(act[5]),int(-act[6]))
            # print size[1]/2,size[0]/2
            cv2.line(self.frame,(size[1]/2,size[0]/2),((size[1]/2)+c[0],(size[0]/2)+c[1]),(255,0,0),2)
 #           coord_hist = (act[1],act[3])

            if act[7] is not None:  # no face found
                self.steer_to(act[5], act[6], act[7])
            
            vis = self.frame.copy()
            hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))

            if self.selection:
                x0, y0, x1, y1 = self.selection
                self.track_window = (x0, y0, x1-x0, y1-y0)
                hsv_roi = hsv[y0:y1, x0:x1]
                mask_roi = mask[y0:y1, x0:x1]
                hist = cv2.calcHist( [hsv_roi], [0], mask_roi, [16], [0, 180] )
                cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
                self.hist = hist.reshape(-1)
                self.show_hist()

                vis_roi = vis[y0:y1, x0:x1]
                cv2.bitwise_not(vis_roi, vis_roi)
                vis[mask == 0] = 0

            if self.tracking_state == 1:
                self.selection = None
                prob = cv2.calcBackProject([hsv], [0], self.hist, [0, 180], 1)
                prob &= mask
                term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
                for i,value in enumerate(self.track_window):
                    if value<=0:
                        #print i,value
                        self.track_window = (0,0,1000,1000)
                        break
                #print self.track_window
                track_box, self.track_window = cv2.CamShift(prob, self.track_window, term_crit)
                
                if self.show_backproj:
                    vis[:] = prob[...,np.newaxis]
                try:
                    cv2.ellipse(vis, track_box, (0, 0, 255), 2)
                except:
                    pass
                    # print track_box

            cv2.imshow(self.window_name, vis)

            ch = 0xFF & cv2.waitKey(50)
            if ch == 27:
                break
            if ch == ord('b'):
                self.show_backproj = not self.show_backproj
        cv2.destroyAllWindows()
        print "video loop stopped."

    def run_new(self):
        import cv2.cv as cv
        while self.running:
            pixelarray = self.drone.get_image() # get an frame form the Drone
            if pixelarray is not None: # check whether the frame is not empty
                self.frame = pixelarray[:, :, ::-1].copy() #convert to a frame

            weirdsize = self.frame.shape
            size = (weirdsize[1], weirdsize[0])

            image = cv.CreateImageHeader(size[:2], cv.IPL_DEPTH_8U, 3)
            cv.SetData(image, self.frame, size[0]*3)

            # Grab centroid and faces
            ctr, faces = face_tracker.track(image)
            faces = [f for (f, n) in faces]

            # print "got %s faces" % str(len(faces))

            gotface = True
            face = None
            bestface = None
            if self.lastface is None:  # no previous data, wait until only one face detected
                if len(faces) == 1:
                    self.lastface = faces[0]
                    face = faces[0]
                else:
                    # print "no face yet"
                    gotface = False
            else:
                # we have previous face data
                if len(faces) == 0:
                    self.consequtive_misses += 1
                    gotface = False
                else:
                    # look for the best face
                    for item in faces:
                        (x, y, w, h) = item
                        # print "face at ", x, " ", y
                        facediff = tuple_absolute_difference(item, self.lastface)
                        avg_diff = sum(facediff) / len(facediff)
                        if bestface is None or avg_diff < bestface[1]:
                            bestface = (item, avg_diff)
                            # print "reassign: avgdiff=", avg_diff

                    if bestface is None or bestface[1] > 30.0:
                        # ignore improbable face movement
                        self.consequtive_misses += 1
                    else:
                        face = bestface[0]

                if self.consequtive_misses > 10:
                    self.consequtive_misses = 0
                    print "20 misses, resetting face detector"
                    self.lastface = None
            if gotface:
                # draw all faces
                for item in faces:
                    (x, y, w, h) = item
                    if item == face:
                        cv.Rectangle(image, (x, y), (x+w, y+h), cv.RGB(255, 0, 0), 3, 8, 0)
                    else:
                        cv.Rectangle(image, (x, y), (x+w, y+h), cv.RGB(0, 0, 255), 3, 8, 0)

                if face is not None:
                    # steer and draw steering line
                    (fx, fy, fw, fh) = face
                    framecenter = (size[0] / 2, size[1] / 2)
                    center = (fx + fw / 2, fy + fh / 2)
                    dx = center[0] - framecenter[0]
                    dy = center[1] - framecenter[1]
                    cv2.line(self.frame, framecenter, center, (0, 255, 0), 4)
                    self.steer_to(dx, dy, (fw, fh))
                    self.lastface = face

            cv2.imshow(self.window_name, self.frame)
            time.sleep(0.05)

        cv2.destroyAllWindows()
        print "video loop stopped."

def bound(val, maxval=1.0):
    return max(0, min(val, maxval))

class ccontroller:
    def __init__(self):
        pass

    def adjust(self, x, y, z):
        if x < X_LOWER:
            return "turnleft", 0.15
        elif x > X_UPPER:
            return "turnright", 0.15
        elif z < Z_LOWER:
            return "up", 0.4
        elif z > Z_UPPER:
            return "down", 0.4
        elif y > Y_UPPER:  # too big, move away
            return "backward", 0.05
        elif y < Y_LOWER:
            return "forward", 0.05
        else:
            return "hover", 0.3

class Pcontroller:
    def __init__(self):
        pass

    def adjust(self, x, y, z):
        if x < X_LOWER:
            return "turnleft", bound(abs(x) / 320.0 * 0.5)
        elif x > X_UPPER:
            return "turnright", bound(abs(x) / 320.0 * 0.5)
        elif z < Z_LOWER:
            return "up", bound(abs(z - Z_CENTER) / 160.0 * 0.9)
        elif z > Z_UPPER:
            return "down", bound(abs(z - Z_CENTER) / 160.0 * 0.9)
        elif y > Y_UPPER:  # too big, move away
            return "backward", bound(abs(y - Y_CENTER) / 30.0 * 0.15, 0.15)
        elif y < Y_LOWER:
            return "forward", bound(abs(y - Y_CENTER) / 20.0 * 0.15, 0.15)
        else:
            return "hover", 0.3

def xnorm(x):
    return abs(x) / 320.0

def ynorm(y):
    return abs(y - Y_CENTER) / 30.0

def znorm(z):
    return abs(z - Z_CENTER) / 160.0

class PDcontroller:
    def __init__(self):
        self.lastxs = collections.deque(maxlen=5)
        self.kp = 0.05
        self.kd = 0.05

    def adjust(self, x, y, z):
        if x < X_LOWER:
            return "turnleft", bound(abs(x) / 320.0 * 0.5)
        elif x > X_UPPER:
            return "turnright", bound(abs(x) / 320.0 * 0.5)
        elif z < Z_LOWER:
            return "up", bound(abs(z - Z_CENTER) / 160.0 * 0.9)
        elif z > Z_UPPER:
            return "down", bound(abs(z - Z_CENTER) / 160.0 * 0.9)
        elif y > Y_UPPER:  # too big, move away
            return "backward", bound(abs(y - Y_CENTER) / 30.0 * 0.15, 0.15)
        elif y < Y_LOWER:
            return "forward", bound(abs(y - Y_CENTER) / 20.0 * 0.15, 0.15)
        else:
            return "hover", 0.3



class PIDcontroller:
    def __init__(self):
        pass

    def adjust(self, x, y, z):
        return "hover", 0.3




#if __name__ == '__main__':
#    import sys
#    try:
#        video_src = sys.argv[1]
#    except:
#        video_src = 0
#    print __doc__
#    AF(video_src).run()




#drone=libardrone.ARDrone(1,1) #initalize the Drone Object
#running = True
#while running:
#    try:
#        # This should be an numpy image array
#        pixelarray = drone.get_image() # get an frame form the Drone
#        if pixelarray != None: # check whether the frame is not empty
#            frame = pixelarray[:, :, ::-1].copy() #convert to a frame
#            # Display the Image
#            cv2.imshow('Drone', frame) # show the frame
#            if cv2.waitKey(1) & 0xFF == 27: #stop with esc
#            # escape key pressed
#                running = False
#        else:
#            print "empty frame"
#    except:
#        print "Failed"
#        running = False
#        
#print "sending halt"
#drone.halt()