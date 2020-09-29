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

#Program Setup
#initalize roscore node
rospy.init_node('wall_follow_control_node')
#initalize a publisherto publish drive commands to the robot
commandPublisher = rospy.Publisher('/cmd_vel',Twist,queue_size = 10)
#initalize a subscriber to retrieve laser data
#laserSubscriber = rospy.Subscriber('/stable_scan',LaserScan,courseCorrect)

#initalize Variables
#message variables
#only change the x of the linear velocity
msgLinVel = Vector3(0.1,0.0,0.0)
#only change the z of the rotational velocity
msgRotVel = Vector3(0.0,0.0,0.0)
#create message
msg = Twist(linear = msgLinVel,angular = msgRotVel)

commandPublisher.publish(msg)

delay = rospy.Rate(.5)

#define the callbackfunction which pulls the desired laser values and updates the stored variables
def courseCorrect(scanData):

    #filter out garbage values like constant offset around 135
    if scanData.ranges.index(max(scanData.ranges)) > 135 or scanData.ranges.index(max(scanData.ranges)) < 128:
        
        #find angle of closest point in laser data
        idx = scanData.ranges.index(min(scanData.ranges))

        #course correct to put point in front of robot (180 deg)
        if idx > 180:
            msg.angular = Vector3(0.0,0.0,-0.5)
        elif idx < 180:
            msg.angular = Vector3(0.0,0.0,0.5)
        else:
            msg.angular = Vector3(0.0,0.0,0.0)

        #send the correction to the robot
        commandPublisher.publish(msg)
        
#pull laser data from scanner
laserSubscriber = rospy.Subscriber('/scan',LaserScan,courseCorrect)
rospy.spin()
