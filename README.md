# warmup_project
This is Timothy Novak's repo for the Olin Computational Robotics warmup project.

## Structure:
- Scripts:

	This folder contains all of the python scripts that dictate the various behaviors of a simulated Neato Robot.

- Bags:

	This folder contains bag files from trial robot operations. A Bag file contains all of the sensor data from a simulation of a robot.

## Executing the files in this repository

[Instructions on how to run robot sim and scripts]

## Robot Behaviors modeled

	This repo contains a set of scripts which dictate how the simulated Neato robot should respond to input and its environment. Information about each of the behaviors can be found below.

- ### Teleoperated Mode
	This mode is where the user directly controlls the bahavior of the robot through keyboard commands. The robot identifies the w,a,s,d keys as valid inputs and will move forward, turn left, move backward, and turn right respectively, when the keys are pressed. if any other key other than w,a,s,or d is pressed the robot will stop. If multiple keys are pressed the robot will execute all of the commands i.e. pressing w and a will execute as a left turn while driving straight where merely pressing a will execute a turn in place.
	[TODO: Add Gif]

- ### Trace Square Mode
	This mode is where the robot automatically traces out a square. The robot uses the onboard clock to calculate the distances and ammounts it should be turning. It drives forward for 2 seconds at half a meter per second then it turns for one second at pi/2 rad/sec and it repeats this four times to draw a square.
	[TODO: Add Gif]
	As you can see the robot is not very accurate at drawing a square. it tends to 'drift' throughout the process. This is caused by inconsistancies in the robot's speed or onboard time sensing.So an improvement that could be madeto this program is that instead of relying on a time based count to determine distance and turn angle, switching to rely on the data provided by the wheel encoders. Using wheel encoder data would allow the robot to measure how many rotations each of its wheels actually took so that it can move more precisely.

- ### Wall Following Mode
