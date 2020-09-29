#! /usr/bin/env python3
"""This program will drive a simulated Neato following a wall"""

#imports
#ROS imports
#import ros message format accepted by the robot
from geometry_msgs.msg import Twist
#import data types to go in the message
from geometry_msgs.msg import Vector3
#import laser scanner datatype
from sensor_msgs.msg import LaserScan
#import ros functions
import rospy
#import pi value
from math import pi
#Keyboard input imports
import tty 
import select
import sys 
import termios

#Program Setup
#initalize roscore node
rospy.init_node('wall_follow_control_node')
#initalize a publisher to publish drive commands to the robot
commandPublisher = rospy.Publisher('/cmd_vel',Twist,queue_size = 10)
#setup the keyboard listener
settings = termios.tcgetattr(sys.stdin)


#initalize Variables
#message variables
#only change the x of the linear velocity
msgLinVel = Vector3(0.0,0.0,0.0)
#only change the z of the rotational velocity
msgRotVel = Vector3(0.0,0.0,0.0)
#create message
msg = Twist(linear = msgLinVel,angular = msgRotVel)
#get the robot moving forward
commandPublisher.publish(msg)
#define state variable
state = "teleop"

#function definitions
#supplied function which will get a key from the keyboard

def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

#code pulled from teleop.py
#define the callbackfunction which pulls the desired laser values and updates the stored variables
def courseCorrect(scanData):

    #set up variables
    global state
    key = getKey()

    if key == "t":
        if state == 'tracker':
            
            #teleop 
            state = 'teleop'        

        else:
             
            state = 'tracker'

    if state == 'teleop': 
        #update the message sent to the robot to reflect the keyboard commands
        if key == "w":
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

    if state == "track":    
        #filter out the garbage values which seem to be a constant error around         130 degrees
        if scanData.ranges.index(max(scanData.ranges)) > 135 or scanData.ranges.        index(max(scanData.ranges)) < 128:
        
            #find the angle of the closest point in the lidar scan
            idx = scanData.ranges.index(min(scanData.ranges))
            print(idx)
            #turn away from the obstacle
            if idx > 180:
                msg.angular = Vector3(0.0,0.0,-0.5)
            elif idx < 180:
                msg.angular = Vector3(0.0,0.0,0.5)
            else:
                msg.angular = Vector3(0.0,0.0,0.0)

    print(msg)    
    commandPublisher.publish(msg)

delay = rospy.Rate(25)
while getKey() != '\x03': 

    #pull laser range finder data        
    laserSubscriber = rospy.Subscriber('/scan',LaserScan,courseCorrect)
    delay.sleep()
