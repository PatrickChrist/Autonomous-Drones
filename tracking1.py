# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 17:32:35 2015

@author: johannes
"""

import libardrone.libardrone as libardrone #import the libardone 
import numpy as np
import cv2 #import opencv

drone=libardrone.ARDrone(1,1) #initalize the Drone Object 1=ardrone 2, 1=hd stream
running = True
imgcounter = 0

while running:
    try:
        # This should be an numpy image array
        drone.set_camera_view(True) 
    
      #key = cv2.waitkey
        
      #webcam ansteuern über videocapture(0) oder so
      #pixelarray = drone.get_image() # get an frame form the Drone
        pixelarray = drone.get_image() # get an frame form the Drone
        frameRGB = pixelarray[:, :, ::-1].copy()
        frame = cv2.cvtColor(frameRGB, cv2.COLOR_RGB2GRAY);
        #frameRGB = cv2.imread("drone_frame11.jpg")  
        #frame = cv2.cvtColor(frameRGB, cv2.COLOR_RGB2GRAY);

      #read image            
        """try: 
            # frame = cv2.imread("drone_frame11.jpg",0)  
            # frameRGB = cv2.imread("drone_frame11.jpg")  
            frame = cv2.imread("ball2.png",0)  
            frameRGB = cv2.imread("ball2.png") 
            except:
          print "couldnt read image"
        """        
        #create videowriter
      #height, width, layers = pixelarray.shape
      #video = cv2.VideoWriter('video_drone.avi',-1,1,(width,height))
          
      #if pixelarray != None: # check whether the frame is not empty
        if frame != None: # check whether the frame is not empty
                #frame = pixelarray[:, :, ::-1].copy() #convert to a frame
                # Write image to video
                #video.write(frame)            
                #print "could read frame"
    
                #detect circle
                #frametmp = cv2.COLOR_RGB2GRAY(frame)
                #reduce noise
                frametmp = cv2.medianBlur(frame,5)
                #frametmp = cv2.cvtColor(frametmp, cv2.COLOR_GRAY2BGR)
                #frametmp = cv2.cvtColor(frametmp, cv2.COLOR_RGB2GRAY)
                
                #frametmp = cv2.cvtColor(frametmp,cv2.COLOR_GRAY2BGR)
                #param1: higher treshold of canny edge detector
                #param2: accumulator treshold for circle center. The smaller it is, the more small circles are detected
                #circles = cv2.HoughCircles(frametmp,cv2.CV_HOUGH_GRADIENT,1,20, param1=100,param2=100,minRadius=0,maxRadius=0)   
                circles = cv2.HoughCircles(frametmp,3 ,1,800, param1=30,param2=40,minRadius=100,maxRadius=1000)            
                #circles = numpy.uint16(numpy.around(circles))
                      
                
                if circles != None:
                    
                    for i in circles[0,:]:
                        #draw the outer circle
                        cv2.circle(frameRGB,(i[0],i[1]),i[2],(0,255,0),2)
                    # draw the center of the circle
                        cv2.circle(frameRGB,(i[0],i[1]),2,(0,0,255),3)
                
                #frame = frametmp
                # Display the Image
                cv2.imshow('Drone', frameRGB) # show the frame
    
                """if cv2.waitKey(1) & 0xFF == 32: # detect space key press  
                    print "key pressed"
                    #namestring = "drone_frame"
                    #print namestring
                    imgcounter=imgcounter+1
                    namestring = "drone_frame" +str(imgcounter)+".jpg"
                    #save image                
                    cv2.imwrite(namestring, frame)
                    """
                #else:
                    #print "nothing"
                
                if cv2.waitKey(1) & 0xFF == 27: #stop with esc
                # escape key pressed
                    #running = False
                    cv2.destroyAllWindows()
                    #frame.release()
                    #frametmp.release()
                    #frameRGB.release()
                    break
                    #video.release()

    except:
        print "Failed"