##### Suggested clean drone startup sequence #####
import time, sys
import ps_drone                                              # Import PS-Drone
import cv2

drone = ps_drone.Drone()                                     # Start using drone
drone.startup()                                              # Connects to drone and starts subprocesses

drone.reset()                                                # Sets drone's status to good (LEDs turn green when red)
while (drone.getBattery()[0] == -1):      time.sleep(0.1)    # Waits until drone has done its reset
print "Battery: "+str(drone.getBattery()[0])+"%  "+str(drone.getBattery()[1])	# Gives a battery-status
drone.useDemoMode(True)                                      # Just give me 15 basic dataset per second (is default anyway)

##### Mainprogram begin #####
drone.setConfigAllID()                                       # Go to multiconfiguration-mode
drone.sdVideo()             
#drone.videoFPS(60)                      # Choose lower resolution (hdVideo() for...well, guess it)
drone.frontCam()                                             # Choose front view
CDC = drone.ConfigDataCount
while CDC == drone.ConfigDataCount:       time.sleep(0.0001) # Wait until it is done (after resync is done)
#drone.startVideo()                                           # Start video-function
#drone.showVideo()                                            # Display the video


cam = cv2.VideoCapture('tcp://192.168.1.1:5555')
print "Created VideoCapture"
running = True
while running:    # get current frame of video    
    running, frame = cam.read()    
    if running:    
		# cv2.rectangle(frame, (x1, y1), (x2, y2), (255,0,0), 2)    
        cv2.imshow('frame', frame)        
        if cv2.waitKey(1) & 0xFF == 27:             # escape key pressed            
            running = False    
        else:        # error reading frame        
		print 'error reading video feed'
  
cam.release()
cv2.destroyAllWindows()
