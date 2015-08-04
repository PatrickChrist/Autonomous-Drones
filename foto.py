# -*- coding: utf-8 -*-

import libardrone.libardrone as libardrone #import the libardrone 
import cv2 #import opencv

drone=libardrone.ARDrone(1,1) #initalize the Drone Object
#floor camera
drone.set_camera_view(0)
imgcounter = 1

running = True
while running:
    try:
        # This should be a numpy image array
        pixelarray = drone.get_image() # get a frame form the Drone
        if pixelarray != None: # check whether the frame is not empty
            frame = pixelarray[:, :, ::-1].copy() #convert to a frame
  
            # Display the Image
            cv2.imshow('Falco Drone', frame) # show the frame
            #cv2.imshow("Folce with Color Detection", np.hstack([frame, output]))
            if cv2.waitKey(1) & 0xFF == 27: #stop with esc
            # escape key pressed
                running = False
            
            if cv2.waitKey(1) & 0xFF == 32: # detect space key press  
                print "key pressed"
                #namestring = "drone_frame"
                #print namestring
                imgcounter=imgcounter+1
                namestring = "drone_frame" +str(imgcounter)+".jpg"
                #save image                
                cv2.imwrite(namestring, frame)

    except:
        print "Failed"
