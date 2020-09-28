#! /usr/bin/env python4
"""This program will perform drive a simulated Neato in a square pattern"""

#imports
#ROS imports
#import ros message format accepted by the robot
from geometry_msgs.msg import Twist
#import data types to go in the message
from geometry_msgs.msg import Vector3
#import ros functions
import rospy
#import pi value
from math import pi

#Program Setup
#initalize roscore node
rospy.init_node('square_drive_control_node')
#initalize a publisherto publish drive commands to the robot
commandPublisher = rospy.Publisher('/cmd_vel',Twist,queue_size = 10)

#initalize Variables
#message variables
#only change the x of the linear velocity
msgLinVel = Vector3(0.0,0.0,0.0)
#only change the z of the rotational velocity
msgRotVel = Vector3(0.0,0.0,0.0)
#create message
msg = Twist(linear = msgLinVel,angular = msgRotVel)

#loop through the full times to draw the square
for squareIdx in range(2):

    #draw the square
    #loop through the sides of the square
    for sideIdx in range(4):
        #drive forward 1 meter
        #set how long it will take to do this
        forwardTime = rospy.Rate(.5)
        #create a single iteration loop so rospy will time limit the loop and get the robot to move forward for one meter based on time and speed
        for fowardTimeIdx in range(1):
            #set the robot speed
            msg.linear = Vector3(0.5,0.0,0.0)
            #send the message to the robot
            commandPublisher.publish(msg)
            #drive forward for the set time
            forwardTime.sleep()
        #stop the robot
        msg.linear = Vector3(0.0,0.0,0.0)
        commandPublisher.publish(msg)
        #set the time for the turn
        turnTime = rospy.Rate(1)
        #create a single iteration loop so rospy can time limit the turns
        for rotTimeIndx in range(1):
            #set the angular velocity of the robot
            msg.angular = Vector3(0.0,0.0,pi/2)
            commandPublisher.publish(msg)
            #turn for the set time
            turnTime.sleep()
        #stop robot
        msg.angular = Vector3(0.0,0.0,0.0)
        commandPublisher.publish(msg)
