import numpy as np
import cv2
import matplotlib.pyplot as plt
import libardrone
import time
import os
from skimage import measure
from skimage import morphology
from skimage import data
from skimage import filter
from collections import Counter
#import ps drones

class PythonOpenCVTests:
    """A testbed for Python-OpenCV classes"""
    i = 12345
    frame = None
    roiPts = []
    inputMode = False

    def utilResizeImgIsoScale(self,frame,scale=0.5):
        frame = cv2.resize(frame,None,fx=scale, fy=scale, interpolation = cv2.INTER_LINEAR)
        return frame
    def utilSelectROI(self,event, x, y, flags, param):
        # grab the reference to the current frame, list of ROI
        # points and whether or not it is ROI selection mode
        #global frame, roiPts, inputMode

        # if we are in ROI selection mode, the mouse was clicked,
        # and we do not already have four points, then update the
        # list of ROI points with the (x, y) location of the click
        # and draw the circle
        if self.inputMode and event == cv2.EVENT_LBUTTONDOWN and len(self.roiPts) < 4:
            self.roiPts.append((x, y))
            cv2.circle(self.frame, (x, y), 4, (0, 255, 0), 2)
            cv2.imshow("frame", self.frame)
    def testColorFilterVideo(self,c_target=np.uint8([[[153, 111, 98]]]),c_tolerance=30):
        # filter color in webcam video
        # (optional) parameters:
        #   c_target is the target color that we want to segment/detect
        #   c_tolerance is the tolerance of color range that we want to track (in H(SV) space)
        #   --> in effect, we track color in H-channel between c_target +/- c_tolerance
        cap = cv2.VideoCapture(0)

        flagScreenshotSaved = False

        while(1):
            # Take each frame
            _, frame = cap.read()
            # denoise
            frame = cv2.resize(frame,None,fx=0.3, fy=0.3, interpolation = cv2.INTER_LINEAR)
            frame = cv2.fastNlMeansDenoisingColored(frame,None,3,3,7,7)
            # Convert BGR to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
            # define range of blue color in HSV
            hsv_targetcolor = cv2.cvtColor(c_target,cv2.COLOR_RGB2HSV)
            c_lower = np.array([np.maximum(hsv_targetcolor[0,0,0]-c_tolerance, 0), 50, 50])
            c_upper = np.array([np.minimum(hsv_targetcolor[0,0,0]+c_tolerance,179), 255, 255])
            # Threshold the HSV image to get only blue colors
            mask = cv2.inRange(hsv, c_lower, c_upper)
            # post-process mask
            #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))
            #opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            # Bitwise-AND mask and original image
            res = cv2.bitwise_and(frame,frame, mask=mask)
            cv2.imshow('frame',frame)
            cv2.imshow('mask',mask)
            cv2.imshow('res',res)
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break
        cap.release()
        cv2.destroyAllWindows()
    def testGeometricTransformationPicture(self,filename='/Users/mangotee/Pictures/mrSpex2.jpg'):
        img = cv2.imread(filename)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        rows,cols,ch = img.shape

        pts1 = np.float32([[56,65],[328,52],[28,387],[389,360]])
        pts2 = np.float32([[0,0],[300,0],[0,300],[300,300]])

        M = cv2.getPerspectiveTransform(pts1,pts2)

        dst = cv2.warpPerspective(img,M,(300,300))

        plt.subplot(121),plt.imshow(img),plt.title('Input')
        plt.subplot(122),plt.imshow(dst),plt.title('Output')
        plt.show()
    def testFaceDetectionVideo(self):
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

        cap = cv2.VideoCapture(0)

        flagScreenshotSaved = False

        while(1):

            # Take each frame
            _, frame = cap.read()
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            #print cap.get(cv2.cv.CV_CAP_PROP_FPS)

            # denoise
            #frame = cv2.resize(frame,None,fx=0.3, fy=0.3, interpolation = cv2.INTER_LINEAR)

            faces = face_cascade.detectMultiScale(frame, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                eyes = eye_cascade.detectMultiScale(roi_gray)
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

            cv2.imshow('res',frame)
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break
        cap.release()
        cv2.destroyAllWindows()
    def testReadDroneVideofeedOpencv(self):
        cam = cv2.VideoCapture('tcp://192.168.1.1:5555')
        running = True
        while running:
            # get current frame of video
            running, frame = cam.read()
            if running:
                cv2.imshow('frame', frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    # escape key pressed
                    running = False
            else:
                # error reading frame
                print 'error reading video feed'
        cam.release()
        cv2.destroyAllWindows()
    def testDroneConnection(self):
        # read battery status, extract an image
        drone = libardrone.ARDrone(1,0)
        drone.reset()
        '''
        I = drone.image
        if I != None:
            frame = I[:, :, ::-1].copy()
        # You might need to call drone.reset() before taking off if the drone is in
        # emergency mode

        # get battery status
        bat = drone.navdata.get(0, dict()).get('battery', 0)
        print bat

        # get an image
        #while(1):
        img = drone.image
        cv2.imwrite('/Users/mangotee/Pictures/imgDroneOut.png',img)

        # test flying
        #drone.takeoff()
        #drone.land()
        #drone.halt()
        '''

        running = True
        bat = drone.navdata.get(0, dict()).get('battery', 0)
        print('Battery: %i%%' % bat)
        counter=1
        while running:
            try:
                # This should be an numpy image array
                pixelarray = drone.get_image()
                frame = pixelarray[:, :, ::-1].copy()
                if pixelarray != None:
                    #print "problem"
                    #frame = drone.image
                    # Display the Image
                    pass
                if counter==1:
                    cv2.imwrite('/Users/mangotee/Pictures/imgDroneOut.png',frame)
                    counter=counter+1
                cv2.imshow('Drone', frame)
                #print "Success"
            except:
                pass
                #print "Failed"
            '''
            if cv2.waitKey(1) & 0xFF == ord('w'):
            print "Take OFF!!"
            drone.reset()
            drone.takeoff()
            drone.hover()
            '''
            # Listen for Q Key Press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                running = False
        cv2.destroyAllWindows()
    def testTrackGreenBallFromVideoFile(self):
        cap = cv2.VideoCapture('/Users/mangotee/Dropbox/Teaching/CDTM ARdrones Lecture/vid_TrackColoredBall.mov')
        while(cap.isOpened()):
            ret, frame = cap.read()
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            fromRGB = False
            if fromRGB:
                c_target = np.array([[[115, 215, 160]]], np.uint8) # green ball
                #c_target = np.array([[[70, 70, 100]]], np.uint8) # redbrick wall
                #c_target = np.array([[[255, 0, 0]]], np.uint8) # blue shirts
                c_tolerance = 27
                hsv_target = cv2.cvtColor(c_target,cv2.COLOR_BGR2HSV)
                c_lower= np.array([np.maximum(hsv_target[0,0,0]-c_tolerance, 0), 50,50], np.uint8)
                c_upper= np.array([np.minimum(hsv_target[0,0,0]+c_tolerance, 179), 255,255], np.uint8)
            else:
                c_lower = np.array([0, 0, 0])
                c_upper = np.array([179, 255, 255])
            mask = cv2.inRange(hsv, c_lower, c_upper)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15))
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

            # Bitwise-AND mask and original image
            res = cv2.bitwise_and(frame,frame, mask=mask)

            #cv2.imshow('frame',frame)
            cv2.imshow('mask',mask)
            cv2.imshow('result',res)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    def utilFilterColorRGB(self, img, c_bgr=np.array([153, 111, 98]),c_tolerance=20):
        c_target=np.uint8([[[c_bgr[0], c_bgr[1], c_bgr[2]]]])
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        hsv_target = cv2.cvtColor(c_target,cv2.COLOR_BGR2HSV)
        print c_bgr
        print hsv_target
        c_lower = np.array([np.maximum(hsv_target[0,0,0]-c_tolerance, 0), 50, 50])
        c_upper = np.array([np.minimum(hsv_target[0,0,0]+c_tolerance,255), 255, 255])
        mask = cv2.inRange(hsv, c_lower, c_upper)
        return mask
    def utilCvColorOpenCV2Matplotlib(self,img):
        img2 = np.fliplr(img.reshape(-1,3)).reshape(img.shape)
        return img2
    def demoMorphologicalOperationsImage(self, filename='/Users/mangotee/Dropbox/Teaching/CDTM ARdrones Lecture/imgTennisBallBed.jpg'):
        img = cv2.imread(filename)
        mask = self.utilFilterColorRGB(img,np.array([0, 255, 255]), 8)
        displayOpenCV = False

        if displayOpenCV:
            cv2.imshow('img',img)
            cv2.imshow('mask',mask)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            #fname = '/Users/mangotee/Dropbox/Teaching/CDTM ARdrones Lecture/imgTennisBallBed_v1_colfilSingle.png'
            #cv2.imwrite(fname,np.uint8(mask))
            maskLargestComponent = self.findLargestComponent(mask)


            fig1 = plt.figure(facecolor='w')
            #fig1.set_tight_layout(True)
            #plt.use('Agg')
            plt.subplot(121),plt.imshow(self.utilCvColorOpenCV2Matplotlib(img)),plt.title('Image')
            plt.axis('off')
            plt.subplot(122),plt.imshow(mask, cmap='gray'),plt.title('Mask')
            plt.axis('off')
            #fname = '/Users/mangotee/Dropbox/Teaching/CDTM ARdrones Lecture/imgTennisBallBed_v1_colfil.png'
            #plt.savefig(fname)
            plt.show()

            fig2 = plt.figure(facecolor='w')
            plt.subplot(131),plt.imshow(self.utilCvColorOpenCV2Matplotlib(img)),plt.title('Image')
            plt.axis('off')
            plt.subplot(132),plt.imshow(mask, cmap='gray'),plt.title('Mask')
            plt.axis('off')
            plt.subplot(133),plt.imshow(maskLargestComponent, cmap='gray'),plt.title('Largest Component')
            plt.axis('off')
            fname = '/Users/mangotee/Dropbox/Teaching/CDTM ARdrones Lecture/imgTennisBallBed_v2_LargestComp.png'
            plt.savefig(fname)
            plt.show()

            # morphological operations on the largest component
            se = morphology.disk(9)
            maskLCmorph = morphology.opening(maskLargestComponent, se)
            maskLCmorph = morphology.closing(maskLCmorph, se)
            fig3 = plt.figure(facecolor='w')
            plt.subplot(131),plt.imshow(self.utilCvColorOpenCV2Matplotlib(img)),plt.title('Image')
            plt.axis('off')
            plt.subplot(132),plt.imshow(maskLargestComponent, cmap='gray'),plt.title('Largest Component')
            plt.axis('off')
            plt.subplot(133),plt.imshow(maskLCmorph, cmap='gray'),plt.title('Opening/Closing')
            plt.axis('off')
            fname = '/Users/mangotee/Dropbox/Teaching/CDTM ARdrones Lecture/imgTennisBallBed_v3_LargestCompMorph.png'
            plt.savefig(fname)
            plt.show()

            # hough circle detection on the image
            circles = cv2.HoughCircles(maskLCmorph, cv2.cv.CV_HOUGH_GRADIENT, 1, param1=200, param2=10, minDist=250, minRadius=80) # and here

            #print "start Hough"
            if circles is not None:
                #print circles
                circles = np.round(circles[0, :]).astype("int")
                for (x, y, r) in circles:
                    print 'x=%0.2f y=%0.2f r=%0.2f' % (x,y,r)
                    cv2.circle(img, (x, y), r, color=[0,0,255], thickness=4)
                    #cv2.rectangle(gray, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

                cv2.imshow('result',img)
                fname = '/Users/mangotee/Dropbox/Teaching/CDTM ARdrones Lecture/imgTennisBallBed_v4_LargestCompMorphWithHoughCircle.png'
                cv2.imwrite(fname,img)
                fname = '/Users/mangotee/Dropbox/Teaching/CDTM ARdrones Lecture/imgTennisBallBed_v4_LargestCompMorph.png'
                cv2.imwrite(fname,maskLCmorph)
    def demoConvolutionFiltersFromFile(self, filename='/Users/mangotee/Dropbox/Teaching/CDTM ARdrones Lecture/imgTennisBallBedCropped.jpg'):
        fnSrc = filename
        img = cv2.imread(fnSrc)
        displayOpenCV = True

        # case1: 3x3 box filter
        s = 15
        kernel = np.ones((s,s),np.float32)/(s*s)
        dst = cv2.filter2D(img,-1,kernel)
        fnOutSuffix = '_case1_%dx%dboxfilter.jpg' % (s, s)
        fnOut = fnSrc.replace('.jpg', fnOutSuffix)
        cv2.imwrite(fnOut,dst)
        cv2.imshow('ConvResult',dst)

        # case2: Gaussian filter
        dst = cv2.GaussianBlur(img,(15,15),9)
        fnOutSuffix = '_case2_%dx%dgaussianfilter.jpg' % (s, s)
        fnOut = fnSrc.replace('.jpg', fnOutSuffix)
        cv2.imwrite(fnOut,dst)
        cv2.imshow('ConvResult',dst)

        maskRaw    = self.utilFilterColorRGB(img,np.array([0, 255, 255]), 8)
        maskSmooth = self.utilFilterColorRGB(dst,np.array([0, 255, 255]), 8)

        hFig = plt.figure(facecolor='w')
        plt.subplot(131),plt.imshow(self.utilCvColorOpenCV2Matplotlib(img)),plt.title('Image')
        plt.axis('off')
        plt.subplot(132),plt.imshow(maskRaw, cmap='gray'),plt.title('Mask of raw')
        plt.axis('off')
        plt.subplot(133),plt.imshow(maskSmooth, cmap='gray'),plt.title('Mask of smoothed')
        plt.axis('off')
        fnOutSuffix = '_case3_colormasksmoothed.jpg'
        fnOut = fnSrc.replace('.jpg', fnOutSuffix)
        plt.savefig(fnOut)
        #plt.show()

        dst = cv2.Sobel(img,-1,1,0, ksize = 3)
        fnOutSuffix = '_case4_sobelx.jpg'
        fnOut = fnSrc.replace('.jpg', fnOutSuffix)
        cv2.imwrite(fnOut,dst)
        cv2.imshow('ConvResult',dst)

        dst = cv2.Sobel(img,-1,0,1, ksize = 3)
        fnOutSuffix = '_case4_sobely.jpg'
        fnOut = fnSrc.replace('.jpg', fnOutSuffix)
        cv2.imwrite(fnOut,dst)
        cv2.imshow('ConvResult',dst)

        dst = cv2.Laplacian(img,-1, ksize = 3)
        fnOutSuffix = '_case5_laplacian.jpg'
        fnOut = fnSrc.replace('.jpg', fnOutSuffix)
        cv2.imwrite(fnOut,dst)
        cv2.imshow('ConvResult',dst)

        dst = cv2.Canny(img, 50, 100)
        fnOutSuffix = '_case6_canny.jpg'
        fnOut = fnSrc.replace('.jpg', fnOutSuffix)
        cv2.imwrite(fnOut,dst)
        cv2.imshow('ConvResult',dst)

        cv2.waitKey(0)

        cv2.destroyAllWindows()
    def findLargestComponent(self,mask):
        print mask.shape
        t = time.time()
        L = measure.label(mask)
        print 'Number of compnents: %d' % np.max(L)
        #fig1 = plt.figure(facecolor='w')
        #plt.subplot(121),plt.imshow(L)
        componentCounts=Counter(L.ravel()).most_common(2)
        elapsed = time.time() - t
        print 'Connected components - Elapsed time: %0.4f s' % elapsed
        return L==componentCounts[1][0]
        #plt.subplot(122),plt.imshow(np.uint8(L==componentCounts[1][0]))
    def demoOtsuThresholding(self):
        img = data.camera()
        thresh = filter.threshold_otsu(img)
        mask = img > thresh

        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8, 2.5), facecolor='w')
        ax1.imshow(img, cmap='gray')
        ax1.set_title('Original')
        ax1.axis('off')

        ax2.hist(img)
        ax2.set_title('Histogram')
        ax2.axvline(thresh, color='r')

        ax3.imshow(mask, cmap='gray')
        ax3.set_title('Thresholded')
        ax3.axis('off')

        fname = '/Users/mangotee/Dropbox/Teaching/CDTM ARdrones Lecture/imgDemoOtsuThresholding.png'
        plt.savefig(fname)

        plt.show()
    def testCamshiftSelectROI(self):
        # from ComputerVisionOnline
        # http://www.computervisiononline.com/blog/tutorial-using-camshift-track-objects-video

        #ap = argparse.ArgumentParser()
        #ap.add_argument("-v", "--video",
        #    help = "path to the (optional) video file")
        #args = vars(ap.parse_args())

        # grab the reference to the current frame, list of ROI
        # points and whether or not it is ROI selection mode
        #global frame, roiPts, inputMode

        # if the video path was not supplied, grab the reference to the
        # camera
        #if not args.get("video", False):
        camera = cv2.VideoCapture(0)

        # otherwise, load the video
        #else:
        #    camera = cv2.VideoCapture(args["video"])

        # setup the mouse callback
        cv2.namedWindow("frame")
        cv2.setMouseCallback("frame", self.utilSelectROI)

        # initialize the termination criteria for cam shift, indicating
        # a maximum of ten iterations or movement by a least one pixel
        # along with the bounding box of the ROI
        termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
        roiBox = None

        # keep looping over the frames
        while True:
            # grab the current frame
            (grabbed, self.frame) = camera.read()
            self.frame = self.utilResizeImgIsoScale(self.frame)

            # check to see if we have reached the end of the
            # video
            if not grabbed:
                break

            # if the see if the ROI has been computed
            if roiBox is not None:
                # convert the current frame to the HSV color space
                # and perform mean shift
                hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
                backProj = cv2.calcBackProject([hsv], [0], roiHist, [0, 180], 1)
                cv2.imshow("backProj",backProj)

                # apply cam shift to the back projection, convert the
                # points to a bounding box, and then draw them
                (r, roiBox) = cv2.CamShift(backProj, roiBox, termination)
                pts = np.int0(cv2.cv.BoxPoints(r))
                cv2.polylines(self.frame, [pts], True, (0, 255, 0), 2)

            # show the frame and record if the user presses a key
            cv2.imshow("frame", self.frame)
            key = cv2.waitKey(1) & 0xFF

            # handle if the 'i' key is pressed, then go into ROI
            # selection mode
            if key == ord("i") and len(self.roiPts) < 4:
                # indicate that we are in input mode and clone the
                # frame
                self.inputMode = True
                orig = self.frame.copy()

                # keep looping until 4 reference ROI points have
                # been selected; press any key to exit ROI selction
                # mode once 4 points have been selected
                while len(self.roiPts) < 4:
                    cv2.imshow("frame", self.frame)
                    cv2.waitKey(0)

                # determine the top-left and bottom-right points
                self.roiPts = np.array(self.roiPts)
                s = self.roiPts.sum(axis = 1)
                tl = self.roiPts[np.argmin(s)]
                br = self.roiPts[np.argmax(s)]

                # grab the ROI for the bounding box and convert it
                # to the HSV color space
                roi = orig[tl[1]:br[1], tl[0]:br[0]]
                roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                #roi = cv2.cvtColor(roi, cv2.COLOR_BGR2LAB)

                # compute a HSV histogram for the ROI and store the
                # bounding box
                roiHist = cv2.calcHist([roi], [0], None, [16], [0, 180])
                roiHist = cv2.normalize(roiHist, roiHist, 0, 255, cv2.NORM_MINMAX)
                roiBox = (tl[0], tl[1], br[0], br[1])

            # if the 'q' key is pressed, stop the loop
            elif key == ord("q"):
                break

        # cleanup the camera and close any open windows
        camera.release()
        cv2.destroyAllWindows()
    def trackColoredBallHoughCircle(self,c_target=np.uint8([[[153, 111, 98]]]),c_tolerance=30):
        cap = cv2.VideoCapture(0)
        while(1):
            # Take each frame
            _, frame = cap.read()
            # resize and smooth
            frame = cv2.resize(frame,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_LINEAR)
            #frame = cv2.fastNlMeansDenoisingColored(frame,None,3,3,7,7)
            #frame = cv2.GaussianBlur(frame,(15,15),3)

            # Convert BGR to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
            # define range of blue color in HSV
            hsv_target = cv2.cvtColor(c_target,cv2.COLOR_RGB2HSV)
            c_lower = np.array([np.maximum(hsv_target[0,0,0]-c_tolerance, 0), 50, 50])
            c_upper = np.array([np.minimum(hsv_target[0,0,0]+c_tolerance,179), 255, 255])
            # Threshold the HSV image to get only blue colors
            mask = cv2.inRange(hsv, c_lower, c_upper)
            # post-process mask
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(15,15))
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            #kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
            #mask = cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, kernel)
            #mask = cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, kernel)
            # Bitwise-AND mask and original image
            res = cv2.bitwise_and(frame,frame, mask=mask)
            #cv2.imshow('frame',frame)
            #cv2.imshow('mask',mask)
            #cv2.imshow('res',res)

            # blur the mask
            maskblurred = mask #cv2.GaussianBlur( mask, (9, 9), 2 )
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            imgtoprocess = maskblurred
            imgtoshow = gray

            #cv2.waitKey(0)

            # the following from:
            # http://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/
            circles = cv2.HoughCircles(imgtoprocess, cv2.cv.CV_HOUGH_GRADIENT, 1, param1=200, param2=10, minDist=250, minRadius=80) # and here

            #print "start Hough"
            if circles is not None:
                #print circles
                circles = np.round(circles[0, :]).astype("int")
                for (x, y, r) in circles:
                    print 'x=%0.2f y=%0.2f r=%0.2f' % (x,y,r)
                    cv2.circle(imgtoshow, (x, y), r, color=255, thickness=4)
                    #cv2.rectangle(gray, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
            cv2.imshow('result',imgtoshow)
            k = cv2.waitKey(5) & 0xFF
            if k == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

tester = PythonOpenCVTests()
doTest = True
if doTest:
    #tester.testColorFilterVideo(c_tolerance=8)
    #tester.testGeometricTransformationPicture()
    #tester.testFaceDetectionVideo()
    #tester.testDroneConnection()
    #tester.testTrackGreenBallFromVideoFile()
    #tester.demoMorphological()
    #tester.demoOtsuThresholding()
    #tester.demoConvolutionFiltersFromFile()
    #tester.testCamshiftSelectROI()
    tester.trackColoredBallHoughCircle(c_target=np.uint8([[[0,255,0]]]),c_tolerance=30)
    print "testbed exited."




