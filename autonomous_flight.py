# -*- coding: utf-8 -*-

import cv2 #import opencv
import video
import numpy as np

class AF(object):
    def __init__(self, video_src, window_name,drone):
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

    def run(self):
        while True:
            # This should be an numpy image array
            pixelarray = self.drone.get_image() # get an frame form the Drone
            if pixelarray != None: # check whether the frame is not empty
                self.frame = pixelarray[:, :, ::-1].copy() #convert to a frame
#            ret, self.frame = self.cam.read()
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
                    print track_box

            cv2.imshow(self.window_name, vis)

            ch = 0xFF & cv2.waitKey(5)
            if ch == 27:
                break
            if ch == ord('b'):
                self.show_backproj = not self.show_backproj
        cv2.destroyAllWindows()


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