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
    frontRightIndex = 180+45
    backRightIndex = 180+15

    if scanData.ranges[frontRightIndex] > 0.01 and scanData.ranges[backRightIndex] > 0.01:
        #set up wall follwing conditionals
        if scanData.ranges[frontRightIndex] > scanData.ranges[backRightIndex]:
            #if the robot is pointint away from the wall turn towards it
            msg.angular = Vector3(0.0,0.0,0.5)
        elif scanData.ranges[backRightIndex] > scanData.ranges[frontRightIndex]:
            #if the robot is pointing towards the wall turn away
            msg.angular = Vector3(0.0,0.0,-0.5)
        else:
            #if the robot is parallel to the wall don't turn
            msg.angular = Vector3(0.0,0.0,0.0)
    else:
        msg.angular = Vector3(0.0,0.0,0.0)
    commandPublisher.publish(msg)

laserSubscriber = rospy.Subscriber('/scan',LaserScan,courseCorrect)
rospy.spin()
