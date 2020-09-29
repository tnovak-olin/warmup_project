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
msgLinVel = Vector3(0.2,0.0,0.0)
#only change the z of the rotational velocity
msgRotVel = Vector3(0.0,0.0,0.0)
#create message
msg = Twist(linear = msgLinVel,angular = msgRotVel)
#get the robot moving forward
commandPublisher.publish(msg)

#define the callbackfunction which pulls the desired laser values and updates the stored variables
def courseCorrect(scanData):

    #filter out the garbage values which seem to be a constant error around 130 degrees
    if scanData.ranges.index(max(scanData.ranges)) > 135 or scanData.ranges.index(max(scanData.ranges)) < 128:
        
        #find the angle of the closest point in the lidar scan
        idx = scanData.ranges.index(min(scanData.ranges))

        #if the point is too close
        if min (scanData.ranges) < 1: 
        
            #turn away from the obstacle
            if idx > 180:
                msg.angular = Vector3(0.0,0.0,0.5)
            elif idx < 180:
                msg.angular = Vector3(0.0,0.0,-0.5)
            else:
                msg.angular = Vector3(0.0,0.0,-0.5)

        #if the point is far away
        else:
            #stop turning
            msg.angular = Vector3(0.0,0.0,0.0)

        commandPublisher.publish(msg)

#pull laser range finder data        
laserSubscriber = rospy.Subscriber('/scan',LaserScan,courseCorrect)
#repeat
rospy.spin()
