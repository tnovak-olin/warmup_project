#!/usr/bin/env python3
"""This program will perform telioperation of a simulated Neato with keyboard input"""

#imports
#ROS imports
#import ros message format accepted by the robot
from geometry_msgs.msg import Twist
#import data types to go in the message
from geometry_msgs.msg import Vector3
#import ros functions
import rospy
#Keyboard input imports
import tty
import select
import sys
import termios

#function definitions
#supplied function which will get a key from the keyboard
def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

#Program Setup
settings = termios.tcgetattr(sys.stdin)
#initalize roscore node
rospy.init_node('teleop_control_node')

#initalize Variables
key = None
#message variables
#only change the x of the linear velocity
msgLinVel = Vector3(0.0,0.0,0.0)
#only change the z of the rotational velocity
msgRotVel = Vector3(0.0,0.0,0.0)
msg = Twist(linear = msgLinVel,angular = msgRotVel)

#while the cntrlc command has not been hit
while key != '\x03':
    
    #get keys from the keyboard
    key = getKey()
    print(key)

    #update the message sent to the robot to reflect the keyboard comands
    if key == None:
        #stop
        msg.linear = Vector3(0.0,0.0,0.0)
        msg.angular = Vector3(0.0,0.0,0.0)
    elif key == "w":
        #forward
        msg.linear = Vector3(0.2,0.0,0.0)
    elif key == "a":
        #left
        msg.angular = Vector3(0.0,0.0,0.2)
    elif key == "s":
        #backward
        msg.linear = Vector3(-0.2,0.0,0.0)
    elif key == "d":
        #right
        msg.angular = Vector3(0.0,0.0,-0.2)
    else:
        #stop
        msg.linear = Vector3(0.0,0.0,0.0)
        msg.angular = Vector3(0.0,0.0,0.0)
    
    print(msg)
