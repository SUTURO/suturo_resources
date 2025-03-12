#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped

"""
For the Carry My Luggage/Help me Carry Challenge:
This little node takes the /poseupdate topic of type PoseWithCovariancecStamped
which is published by hector_slam, and republishes the pose on the 
/global_pose topic of type PoseStamped.
The result is that now the hector_slam localization can be used and no amcl or 
pose_integrator nodes are needed, as long as hector_slam is running."""


def amcl_pose_callback(msg):
    """Callback function to convert PoseWithCovarianceStamped to PoseStamped"""
    global_pose = PoseStamped()

    # Copy header (timestamp & frame_id)
    global_pose.header = msg.header  

    # Copy pose (without covariance)
    global_pose.pose = msg.pose.pose  

    # Publish the converted PoseStamped message
    pub.publish(global_pose)

def main():
    global pub
    rospy.init_node('global_pose_publisher_node', anonymous=True)

    # Publisher for /global_pose
    pub = rospy.Publisher('/global_pose', PoseStamped, queue_size=10)

    # Subscriber to /amcl_pose
    rospy.Subscriber('/poseupdate', PoseWithCovarianceStamped, amcl_pose_callback)

    rospy.loginfo("Global Pose Publisher node started, listening to /poseupdate...")
    rospy.spin()  # Keep the node running

if __name__ == '__main__':
    main()
    



