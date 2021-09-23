#! /usr/bin/env python

import rospy
import numpy as np
from std_srvs.srv import SetBool, SetBoolResponse

from sensor_msgs.msg import LaserScan

class BaseScanLimiterServer:
    """
    Action Server, which limits the laser scanner, when the HSR opens a door.
    """
    IGNORE_AREA = 55
    limit_area = False
    laser_scan_publisher = rospy.Publisher('hsrb/base_scan', LaserScan)
    limit_right_side = True

    def __init__(self, name):
        """
        Inits the action server.
        :param name The name of the action server
        :type name string
        """
        self._action_name = name
        laser_scan_subscriber = rospy.Subscriber('/hsrb/base_scan_unlimited', LaserScan, self.laser_scan_callback)
        service_server = rospy.Service('/base_scan_limitation', SetBool, self.enable_limitation)

    def laser_scan_callback(self, msg):
        """
        Receives the laser data and limits it, when needed.
        :param msg The laser scan message
        :type msg LaserScan
        """
        if self.limit_area:
            sensor_ranges = np.array(msg.ranges)
            sensor_middle = len(sensor_ranges) / 2
            limit_right_length = 0
            limit_left_length = 0
            if self.limit_right_side:
                limit_right_length = self.IGNORE_AREA * 3
                limit_left_length = 120
            else:
                limit_left_length = self.IGNORE_AREA * 3
                limit_right_length = 120
            sensor_ranges[(sensor_middle - limit_left_length):(sensor_middle + limit_right_length)] =\
                [float('inf')] * (limit_left_length + limit_right_length)
            msg.ranges = tuple(sensor_ranges)
        self.laser_scan_publisher.publish(msg)

    def enable_limitation(self, request):
        """
        Enables/Disables the laser scan limitation mechanism.
        :param request data, containing which side to limit
        :type request SetBool
        """
        self.limit_area = not self.limit_area
        self.limit_right_side = request.data
        return SetBoolResponse(
            success = True,
            message = "Limitation is set to: {0}, side: {1}".format(str(self.limit_area), str(self.limit_right_side))
        )


if __name__ == '__main__':
    rospy.init_node('base_scan_limiter')
    server = BaseScanLimiterServer(rospy.get_name())
    rospy.spin()