# rainbow_dash
The approach chosen for Rainbow Dash, is rather simple, and its core, a track-and-follow approach.

The overall goal of passing through three gates is rather daunting, if to be tackled by autonomously detecting all three gates, and determining a flight path based on visual odometry. Instead, a "director" can navigate the drone through the parcour by using a tracking object which the drone follows.

For rainbow dash, a simple checkerboard has been used. Many other project use colored objects or similar artifacts, but this are inherently not very robust if the surrounding scene is complicated and contains similar objects. A structured tracking object, such as a marker (here the checkerboard), can allow for more robust tracking, easier estimate of distance (e.g., if the edge length of a square is known). However, this happens at a higher processing cost, as detecting a checkerboard can be rather complicated, even thought its a rather simple pattern.

Based on the checkerboards centroid in the image frage of the drone's front camera, move commands are generated, and through the ps_drone library given to the drone and executed.

# Usage
The application is simply started via the commandline with no extra parameters. In order to run it, ps_drone library needs to be installed. Also opencv2 (with ffmpeg support) and python bindings needs to be available. Even if no on-screen visualization is used, the stream is processed via opencv2 at the moment.

Basic keyboard instructions can be given to the drone in order to maniplute the flight path, if no checkerboard is given, or a crash is immediate. Should the connection be lost, the drone will automatically initiate the landing sequence. If this should not happen (as unlikely as it is), be aware of the situation and if possible catch the drone by hands and flip it over to trigger the safety-shut down!

Keyboard Commands:

# Steering


# Algorithm and Behaviour
The behavior is easily described. The drone uses its front camera to detect a checkerboard. The centroid of the checkerboard is known, and can easily be calculated from the detected corners. The drone will try to keep the centroid in the center of the image frame (through rotation and flying up and down). Based on the outer-most square (connecting the outermost corners), one can estimate a pseudo-distance (actual distance in cm is not required), and from this one can generate movements to draw the drone closer or push it away.

In order to avoid (read: minimize) oscillation, a PID controller is used to improve the magnitude of the movement speeds. This is a very simple implementation, which does NOT account for delay in the system, inaccurate movement execution, or any other deterioating commands.
