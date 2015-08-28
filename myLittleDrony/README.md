# My Little Drony

This approach uses two different detection stages. The Drone will first search for a circle in its field of view, using the HoughCircle detection algorithm from OpenCV. If a circle is found and remains roughly at the same spot for a given time, the tracking stage is initialized. For this, we use the CamShift algorithm: A rectangular region inside the circle is analyzed for its color or brightness distribution.
From this point, the image is constantly scanned for the current best match to that first identifying distribution.
The drone will then follow the tracking object, which could, for example, be a colored ball or a flashlight.

# Usage

The code allows a manual override of the Drone control at any time. Press any steering key to switch to manual mode. Steering:

Key | Action
----- | ------
W/A/S/D | forward, backward, left, right
Q/E | turn right / left
UP/DOWN | arrow keys fly upwards / downwards
SPACE | land / takeoff
Esc | emergency rotor stop (drop like a stone)
T | switch back to autonomous flying after starting / manual override
1 - 4 | Set drone speed to predifned speed increasing speeds
x | Activate the detection stages by starting the circle detection
c | Reset the Autonomous flight mode and revert to hovering if drone is in the air


After startup you will see the front camera livestream in a window. 
At first, the drone will wait for the activation of the autonomous flight mode. This mode can be triggered before or after taking off.
By pressing 'x', the drone will start searching the livestream for circular shapes. By holding the trackable object into tho field of view for around 5 seconds, the drone will save the color distribution of the object. 
Now, the drone will continously scan the image for the object based on its color. If the object is moved away from the horizontal center of the image, the drone will rotate left or right to position the object in the center again.
The size of the initial object bounding box is saved by the program. If the object is coming closer to the camera, the drone will fly backwards until the the object has the initial distance from the drone again. If the object is moved away, the drone will fly forward until the initial distance is reached.


# Background

The autonomous flight is based on the CamShift algorithm. This algorithm converts the image to a HSV color representation and then uses the hue values for the color-based tracking. It should be noted that varying lighting conditions will influence the robustness of the tracking.
As an alternative approach, the brightness channel can be used instead of the hue channel. In this case, the drone can follow a very bright object, e.g. a flashlight. This approach is very robust in dark environments.
In brighter environments, an opaque filter can be applied to the camera to increase the tracking robustness.
