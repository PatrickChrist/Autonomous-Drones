# Flying Fury

This approach uses a Haar Cascade facetracker from OpenCV to track faces. The Drone will follow a certain face around as long as it does not move around too quickly. This should avoid jittering due to false detections substancially.

# Usage

The code allows a manual override of the Drone control at any time. Press any steering key to switch to manual mode. Steering:

- W/A/S/D forward, backward, left, right
- Q/E turn right / left
- UP/DOWN arrow keys fly upwards / downwards
- SPACE land / takeoff
- P emergency rotor stop (drop like a stone)
- T switch back to autonomous flying after starting / manual override

After startup you will see the front camera livestream in a windows. Recognized faces are illustrated by rectangular boxes. The Drone follows the first recognized face as long as it's geometry doesn't change too rapidly. This avoids trouble with non consistent face detection on most occasions. Ignored faces are drawn in blue, the followed face is drawn in red and the green line indicates the drone movement.

# Background

You can adapt the dead zone of the Drone by changing the variables in [autonomous_flight.py](autonomous_flight.py), the controller used for steering can be swapped by using a strategy pattern in the same file.
