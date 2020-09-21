#!/usr/bin/env python3
"""This script creates a sphere in r vis 10 times a second at a set position"""

#imports
from visualization_msgs.msg import Marker
import rospy

#setup
#register rosnode with roscore
rospy.init_node('visualization_messages')
#initalize publisher
visualPublisher = rospy.Publisher('visualization_marker',Marker, queue_size=10)

#lsetup marker contents
visualMarker = Marker();
#denote what frame the cordinates are in
#visualMarker.header.frame_id = "odom";
visualMarker.header.frame_id = "base_link"
#sets the marker shape
visualMarker.type = Marker.SPHERE;
#sets the cordinates of the marker
visualMarker.pose.position.x = 1;
visualMarker.pose.position.y = 2;
visualMarker.pose.position.z = 0;
#sets the scale of the marker
visualMarker.scale.x = 1;
visualMarker.scale.y = 1;
visualMarker.scale.z = 1;
#sets the color and transparency of the marker
visualMarker.color.a = 1.0;
visualMarker.color.r = 1.0;
visualMarker.color.g = 1.0;
visualMarker.color.b = 1.0;

#publish the message 10 times per second
#sets the rate for the loop in hz
r = rospy.Rate(10)
#loop to publish the message repeatedly
while not rospy.is_shutdown():
    #set the time stamp
    visualMarker.header.stamp = rospy.Time.now()
    #publish the value
    visualPublisher.publish(visualMarker);
    #sleep the loop to publish at the proper time
    r.sleep()
