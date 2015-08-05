import libardrone.libardrone as libardrone
import cv2
import numpy 
import camShift  
 
def detectCircle(sameCircleCounter,frameRGB, centerX, centerY, radius):
    centerX_prev = centerX
    centerY_prev= centerY
    radius_prev = radius
    inbox_width_and_height = 0

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
                inbox_width_and_height = 2* numpy.sqrt((radius**2)/2)
                
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
            if  diffRadius< 30 and  diffX< 40 and  diffY< 40:
                sameCircleCounter+=1
            else:
                sameCircleCounter = 0
            print "counter: " + str (sameCircleCounter)
            if sameCircleCounter > 7: 
                print "Call Meanshift now!"
                #left upper corner:
                success = True
                #return (corner_x,corner_y,width,height)
        return (success,frameRGB,sameCircleCounter,centerX,centerY,radius,inbox_width_and_height)

def fly():
    drone.reset()
    running = True
    return_to_hover = False
    flying = False
    stage = 0 #stages: 0=hover, 1=find circle, 1=use camshift
    
    #variables for the circle detector
    counter,centerX,centerY, radius, inbox_width_and_height, initialEdgeLength = 0,0,0,0,0,0  

    while running:
        keyPressed = True
        key = cv2.waitKey(15)

        #if (key!=-1):
            #keyPressed = False
        #   print str(key)        
        if (key==-1):
            keyPressed = False
        #    print str(key)
        if key == 1048603 or key == 27:  # esc
            if flying:
                drone.land()
            cv2.destroyAllWindows()
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
            elif key == ord('x') and stage == 0
                stage = 1
            else:
                if return_to_hover:
                    return_to_hover = False
                    drone.hover()

        frame = get_frame()
        if (frame != None):
            if (keyPressed == False):
                if (stage==1):
                    (success,frame,counter,centerX,centerY,radius,inbox_width_and_height) = detectCircle(counter,frame,centerX,centerY,radius)
                    if (success==True):
                        stage = 2
                        initialEdgeLength = inbox_width_and_height
                        print "Initialize Camshift"
                        camShiftHandler = camShift.CamShift(centerX,centerY,inbox_width_and_height,inbox_width_and_height,frame)               
                        print "go to stage 2"
                elif (stage==2):                    
                    frame, middleX, middleY, minWidth = camShiftHandler.performCamShift(frame)
                    print str(middleX)+" "+str(middleY)+" minWidth: "+str(minWidth)
                    currentEdgeLength = minWidth
                    edgeLengthRatio = 1 - currentEdgeLength/initialEdgeLength #if object is farther away than at the starting time, then the ratio is > 0
                    #rotation
                    drone.speed = 0.6
                    #if middleX < 240:
                    #    drone.turn_left()
                    #elif middleX > 400:
                    #    drone.turn_right()
                    #approach or distance from target object
                    if (edgeLengthRatio > 0.6):
                        drone.spped = 0.2
                        drone.move_forward()
                    elif (edgeLengthRatio < -0.3):
                        drone.speed = 0.2
                        drone.move_backward()
                    else:
                        drone.hover()

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
    drone = libardrone.ARDrone(True, False)
    cv2.imshow('Drone', numpy.zeros((10, 10)))

    try:
        fly()
    except Exception, e:
        print "Going down because of exception.", e
    finally:
        print "Going down on close"
        drone.land()
        cv2.destroyAllWindows()

