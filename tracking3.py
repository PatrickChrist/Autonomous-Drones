import libardrone.libardrone as libardrone
import cv2
import numpy 
import camShift

def callbackMethod(x,y,minWidth):
	print str(x)+" "+str(y)+" last: "+str(minWidth)
 
def detectCircle(sameCircleCounter,frameRGB, centerX, centerY, radius):
    centerX_prev = centerX
    centerY_prev= centerY
    radius_prev = radius
    width = 0
    height = 0
    frame = cv2.cvtColor(frameRGB, cv2.COLOR_BGR2GRAY)
    if frame != None:
        frametmp = cv2.medianBlur(frame,5)
        #find circles
                        #param1: higher treshold of canny edge detector
        #param2: accumulator treshold for circle center. The smaller it is, the more small circles are detected
        circles = cv2.HoughCircles(frametmp,3 ,1,800, param1=30,param2=40,minRadius=100,maxRadius=1000)                               
        
        radius = 0
        success = False
        if circles != None:
            
            for i in circles[0,:]:
                #draw the outer circle
                cv2.circle(frameRGB,(i[0],i[1]),i[2],(0,255,0),2)
                #draw the center of the circle
                cv2.circle(frameRGB,(i[0],i[1]),2,(0,0,255),3)
        #get inner bounding box

            if len(circles) == 1:
                circle=circles[0][0]
                radius = circle[2]
                centerX = circle[0]
                centerY = circle[1]
                width = 2* numpy.sqrt(radius/2)
                height = width
 
                
        #cv2.imshow('Drone', frameRGB) # show the frame"
            
        #check whether the circle didnt change since the last frame
        
        if radius != 0:
            diffRadius = numpy.abs(radius-radius_prev)
            diffX=numpy.abs(centerX-centerX_prev)
            diffY= numpy.abs(centerY-centerY_prev)
            centerX_prev=centerX
            centerY_prev=centerY
            radius_prev=radius
            print "diffRadius: " + str(diffRadius)+ ", diffX: " + str(diffX)+ ", diffY: " + str(diffY) 
            if  diffRadius< 50 and  diffX< 25 and  diffY< 25:
                sameCircleCounter+=1
            else:
                sameCircleCounter = 0
            print "counter: " + str (sameCircleCounter)
            if sameCircleCounter > 10:
                print "Call Meanshift now!"
                #left upper corner:
                corner_x=centerX-width
                cornter_Y=centerY-width
                width = width
                height = height
                success = True
                #return (corner_x,corner_y,width,height)
        return (success,frameRGB,sameCircleCounter,centerX,centerY,radius,width,height)

def fly():
    drone.reset()
    running = True
    return_to_hover = False
    flying = False
    stage = 0 #stages: 0=find circle, 1=init camshift, 2=use camshift
    
    #webcam
    cap = cv2.VideoCapture(0)
    
    
    #variables for the circle detector
    counter,centerX,centerY, radius,width,height = 0,0,0,0,0,0    
    while running:
        keyPressed = True
        key = cv2.waitKey(33)

        #if (key!=-1):
            #keyPressed = False
        #   print str(key)        
        if (key==-1):
            keyPressed = False
        #    print str(key)
        if key == (1048603 or 27):  # esc
            if flying:
                drone.land()
            running = False
            continue
        if key == ord('p'):
            drone.reset()
            continue

        if not flying:
            if key == 1048608 or key==ord(' '):
                drone.takeoff()
                drone.hover()
                flying = True
        else:
            if key == 1048608 or key==ord(' '):
                drone.hover()
                drone.land()
                flying = False
            elif key == 1048695 or key==ord('w'):
                return_to_hover = True
                drone.move_forward()
            elif key == 1048673 or key==ord('a'):
                return_to_hover = True
                drone.move_left()
            elif key == 1048691 or key==ord('s'):
                return_to_hover = True
                drone.move_backward()
            elif key == 1048676 or key==ord('d'):
                return_to_hover = True
                drone.move_right()
            elif key == 1048689 or key==ord('q'):
                return_to_hover = True
                drone.turn_left()
            elif key == 1048677 or key==ord('e'):
                return_to_hover = True
                drone.turn_right()
            elif key == 1113938 or key==2490368:  # up
                return_to_hover = True
                drone.move_up()
            elif key == 1113940 or key==2621440:  # down
                return_to_hover = True
                drone.move_down()
            elif key == 1048625 or key==ord('1'):
                drone.speed = 0.1
            elif key == 1048626 or key==ord('2'):
                drone.speed = 0.3
            elif key == 1048627 or key==ord('3'):
                drone.speed = 0.5
            elif key == 1048628 or key==ord('4'):
                drone.speed = 0.9
            else:
                if return_to_hover:
                    return_to_hover = False
                    drone.hover()

        #frame = get_frame()
        frame = get_frame_(cap)
        if (frame != None):
            if (keyPressed == False):
                if (stage==0):
                    #(found, squareX, squareY, width,height) = detectcircle(frame)
                    (success,frame,counter,centerX,centerY,radius,width,height) = detectCircle(counter,frame,centerX,centerY,radius)
                    print "counter: " + str(counter)
                    if (success==True):
                        stage = 1
                elif (stage==1):
                    print "stage 2"
                    camShiftHandler = camShift.CamShift(centerX,centerY,width,height,cap,callbackMethod)               
                    stage = 2
                    print "go to stage 3"
                elif (stage==2):                   
                    frame = camShiftHandler.performCamShift()
                #else:
                 #   "undefinded stage"        
            show_frame(frame)
 
def get_frame():
    try:
        pixelarray = drone.get_image()  # get an frame form the Drone
        frame = pixelarray[:, :, ::-1].copy()  # convert to a frame
        return frame
    except Exception, ex:
        print "Frame grabbing failed", ex
        return None
    
def get_frame_(cap): 
    try:
        tmpret, frame = cap.read()  # get an frame form the Drone
        return frame
    except Exception, ex:
        print "Frame grabbing failed", ex
        return None

def show_frame(frame):
    try:
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

