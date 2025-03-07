#!/usr/bin/env python
import subprocess
import sys
from time import sleep
import threading

import rospy
from cryptography.x509 import PrecertPoison
from geometry_msgs.msg import PointStamped
from sensor_msgs.msg import CompressedImage, Image
from std_msgs.msg import String
from robokudo_msgs.msg import QueryActionGoal, ObjectDesignator, QueryFeedback, QueryActionResult

log_lock = threading.Lock()

class TopicChecker:
    """
    Class to check if all required topics are transmitting data
    """

    def __init__(self, topics):
        """
        Initialize the TopicChecker object with a dict of topics and their message types
        :param topics: dict of topics and their message types
        """
        self.topics = topics
        self.received_data = {topic: False for topic in self.topics}

    def callback(self, msg, topic):
        """
        Callback function to set the received_data flag to True
        :param msg: message received on the topic
        :param topic: topic on which the message was received
        """
        self.received_data[topic] = True

    def subscribe_to_topics(self):
        """
        Subscribe to all required topics
        """
        rospy.loginfo("Searching and Subscribing to topics...")
        active_topics = get_active_topics()
        topics = []
        failed_topics = []
        for topic, type in self.topics.items():
            if topic in active_topics:
                topics.append(topic)
                try:
                    rospy.Subscriber(topic, type, self.callback, callback_args=topic)
                except KeyError:
                    continue
            else:
                failed_topics.append(topic)
        rospy.loginfo(f"Found and subscribed to topics: {topics}")
        if failed_topics:
            rospy.logwarn(f"Failed to find the following topics: {failed_topics}\n")
        else:
            rospy.loginfo("All topics found and subscribed to.\n")

    def check_data(self):
        """
        Check if data is being transmitted on all required topics
        """
        rate = rospy.Rate(1)  # 1Hz
        while not rospy.is_shutdown():
            failed_transmissions = []
            self.subscribe_to_topics()
            all_received = True
            for topic, received in self.received_data.items():
                if not received:
                    failed_transmissions.append(topic)
                    all_received = False
            result = [data for data, received in self.received_data.items() if received == True]
            rospy.loginfo("Checking for data...")
            rospy.loginfo(f"Received data on topics: {result}")
            if failed_transmissions:
                rospy.logwarn(f"Failed to receive data on topics: {failed_transmissions}\n")
            else:
                rospy.loginfo("All topics are transmitting data.")
                break
            sleep(5)
            rate.sleep()


def get_active_topics():
    """Retrieve the list of currently active topics"""
    try:
        result = subprocess.run(["rostopic", "list"], stdout=subprocess.PIPE, text=True)
        active_topics = result.stdout.split("\n")
        return set(active_topics)
    except Exception as e:
        rospy.logerr(f"Error getting active topics: {e}")
        return set()

challenges = {
    "receptionist": {
        "/robokudo/query/goal": QueryActionGoal,
        "/robokudo/query/result": QueryActionResult,
        "/human_pose": PointStamped,
        "/startListener": String,
        "/nlp_out": String,
        "/audio/audio": String,
    },
    "cml": {
        "/robokudo/query/goal": QueryActionGoal,
        "/robokudo/query/result": QueryActionResult,
        "/human_pose": PointStamped,
        "/audio/audio": String,
    },
    "restaurant": {
        "/robokudo/query/goal": QueryActionGoal,
        "/robokudo/query/result": QueryActionResult,
        "/startListener": String,
        "/nlp_out": String,
        "/audio/audio": String,
    },
}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Check if all required topics are transmitting data")
    parser.add_argument("-c", "--challenge", nargs="+", help="Challenge(s) to check topics for")
    args = parser.parse_args()

    rospy.init_node("check_hsr_topics", anonymous=True)
    topic_checker = TopicChecker(challenges.get(args.challenge[0]))
    topic_checker.check_data()