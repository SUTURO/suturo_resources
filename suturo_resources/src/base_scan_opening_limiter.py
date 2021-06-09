#! /usr/bin/env python

import rospy
import numpy as np
from std_srvs.srv import SetBool, SetBoolResponse

from sensor_msgs.msg import LaserScan

class BaseScanLimiterServer:
    IGNORE_AREA = 30
    limit_area = False
    laser_scan_publisher = rospy.Publisher('hsrb/base_scan', LaserScan)

    def __init__(self, name):
        self._action_name = name
        laser_scan_subscriber = rospy.Subscriber('/hsrb/base_scan_unlimited', LaserScan, self.laser_scan_callback)
        service_server = rospy.Service('/base_scan_limitation', SetBool, self.enable_limitation)


    def laser_scan_callback(self, msg):
        if self.limit_area:
            sensor_ranges = np.array(msg.ranges)
            sensor_middle = len(sensor_ranges) / 2
            sensor_ranges[(sensor_middle - (self.IGNORE_AREA * 3)):sensor_middle + (self.IGNORE_AREA * 3)] =\
                [float('inf')] * (self.IGNORE_AREA * 2 * 3)
            msg.ranges = tuple(sensor_ranges)
        self.laser_scan_publisher.publish(msg)

    def enable_limitation(self, request):
        self.limit_area = request.data
        return SetBoolResponse(
            success = True,
            message = "base_scan_limitation_set"
        )

if __name__ == '__main__':
    rospy.init_node('base_scan_limiter')
    server = BaseScanLimiterServer(rospy.get_name())
    rospy.spin()