# -*- coding: utf-8 -*-

import libardrone.libardrone as libardrone #import the libardrone 
import cv2 #import opencv
import numpy as np

#color detection try 1
# define the list of boundaries
# here it's only red in BGR
boundaries = [
    ([0, 0, 100], [70, 70, 255])
    #([100, 0, 0], [255, 70, 70])
]

drone=libardrone.ARDrone(1,1) #initalize the Drone Object
#bodenkamera
#drone.set_camera_view(0)
running = True
while running:
    try:
        # This should be a numpy image array
        pixelarray = drone.get_image() # get a frame form the Drone
        if pixelarray != None: # check whether the frame is not empty
            frame = pixelarray[:, :, ::-1].copy() #convert to a frame
            # try to peint something on the image
            cv2.rectangle(frame, (100, 100), (200, 200), (255,255,255), 2)
            
            # this is color detecion stuff
            # loop over the boundaries
            for (lower, upper) in boundaries:
                # create NumPy arrays from the boundaries
                lower = np.array(lower, dtype = "uint8")
                upper = np.array(upper, dtype = "uint8")
                
                # find the colors within the specified boundaries and apply
                # the mask
                mask = cv2.inRange(frame, lower, upper)
                output = cv2.bitwise_and(frame, frame, mask = mask)
            
            # print the height into the video
#            text_height = "100"
#            try:
#                drone_data = drone.get_navdata()
#                text_height = "" + drone_data[0]['altitude'] + ""
#                
#            except Exception:
#                drone_data = drone_data
#            print text_height
#            cv2.putText(output, text_height, (100,100), cv2.FONT_HERSHEY_SIMPLEX, 2, 150) #Draw the text

            # Display the Image
            cv2.imshow('Falco Drone', output) # show the frame
            #cv2.imshow("Folce with Color Detection", np.hstack([frame, output]))
            if cv2.waitKey(1) & 0xFF == 27: #stop with esc
            # escape key pressed
                running = False
    except:
        print "Failed"