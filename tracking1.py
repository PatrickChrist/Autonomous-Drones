# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 17:32:35 2015

@author: johannes
"""

import libardrone.libardrone as libardrone #import the libardone 
import cv2 #import opencv

#drone=libardrone.ARDrone(1,1) #initalize the Drone Object 1=ardrone 2, 1=hd stream
running = True
imgcounter = 0

while running:
    try:
        # This should be an numpy image array
        #drone.set_camera_view(False) 
    
      #key = cv2.waitkey
        
      #webcam ansteuern über videocapture(0) oder so
      #pixelarray = drone.get_image() # get an frame form the Drone
      
      #read image            
      try: 
          frame = cv2.imread("drone_frame11.jpg")      
      except:
          print "couldnt read image"
        #create videowriter
      #height, width, layers = pixelarray.shape
      #video = cv2.VideoWriter('video_drone.avi',-1,1,(width,height))
          
      #if pixelarray != None: # check whether the frame is not empty
      if frame != None: # check whether the frame is not empty
            #frame = pixelarray[:, :, ::-1].copy() #convert to a frame
            # Write image to video
            #video.write(frame)            
            

            
            # Display the Image
            cv2.imshow('Drone', frame) # show the frame

            if cv2.waitKey(1) & 0xFF == 32: # detect space key press  
                print "key pressed"
                #namestring = "drone_frame"
                #print namestring
                imgcounter=imgcounter+1
                namestring = "drone_frame" +str(imgcounter)+".jpg"
                #save image                
                #cv2.imwrite(namestring, frame)
                
            #else:
                #print "nothing"
            
            if cv2.waitKey(1) & 0xFF == 27: #stop with esc
            # escape key pressed
                running = False
            #    cv2.destroyAllWindows()
            #    video.release()

    except:
        print "Failed"