#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped


"""
This node republishes the pose from /amcl_pose to /global_pose.
Since amcl only publishes a new pose if the robot has moved a certain distance,
this node will also republish the last known pose with a new timestamp with 5Hz.
"""

# Global variable to store the last known pose
last_pose = None  

def amcl_pose_callback(msg):
    """Callback function to store and publish the latest PoseStamped message."""
    global last_pose
    
    global_pose = PoseStamped()
    global_pose.header = msg.header  # Copy header (timestamp & frame_id)
    global_pose.pose = msg.pose.pose  # Copy pose (without covariance)
    
    last_pose = global_pose  # Store the last known pose

    pub.publish(global_pose)  # Publish immediately when new data arrives

def publish_last_pose(event):
    """Timer callback to republish the last known pose at a fixed rate."""
    if last_pose is not None:
        last_pose.header.stamp = rospy.Time.now()  # Update timestamp
        pub.publish(last_pose)  # Republish with the updated timestamp

def main():
    global pub
    rospy.init_node('amcl_to_global_pose_publisher_node', anonymous=True)

    # Publisher for /global_pose
    pub = rospy.Publisher('/global_pose', PoseStamped, queue_size=10)

    # Subscriber to /amcl_pose
    rospy.Subscriber('/amcl_pose', PoseWithCovarianceStamped, amcl_pose_callback)

    # Create a timer to republish the last known pose at 5 Hz
    rospy.Timer(rospy.Duration(1.0 / 5), publish_last_pose)  # 5 Hz = every 0.2 seconds

    rospy.loginfo("AMCL to Global Pose Publisher node started, listening to /amcl_pose...")
    rospy.spin()  # Keep the node running

if __name__ == '__main__':
    main()

