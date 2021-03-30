#!/usr/bin/env python
import roslib;

roslib.load_manifest('urdfdom_py')
import rospy
from urdf_parser_py.urdf import URDF

import re
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
from geometry_msgs.msg import Point

pytess_installed = False
try:
    import pytess

    pytess_installed = True
except ImportError:
    pytess_installed = False


class Room:
    points = []
    pose = (0, 0, 0)
    color = (0, 0, 0, 0)  # rgba range 0-1
    name = ""
    id_ = 0
    triangled_points = []

    def reset(self):
        self.points = []
        self.pose = (0, 0, 0)
        self.color = (0, 0, 0, 0)  # rgba range 0-1
        self.name = ""
        self.id_ = 0
        self.triangled_points = []

    def __init__(self):
        self.reset()

    def set_color(self, s):
        self.color = (s[0], s[1], s[2], s[3])

    def set_pose(self, s):
        self.pose = (s[0], s[1], s[2])

    def add_point(self, s):  # ${center_x} ${center_y} 0
        # split = s.split(" ")
        print("called ad point")
        self.points.append((s[0], s[1]))

    def to_marker(self, seq):
        marker = Marker()

        marker.header.seq = seq
        marker.header.stamp = rospy.get_rostime()
        marker.header.frame_id = rospy.get_param('~tf_namespace') + "/" + self.name + "_room_center_link"  # TODO
        marker.ns = self.name
        marker.id = self.id_
        marker.type = Marker.TRIANGLE_LIST
        marker.action = Marker.ADD

        marker.pose.position.x = 0
        marker.pose.position.y = 0
        marker.pose.position.z = 0
        marker.pose.orientation.x = 0
        marker.pose.orientation.y = 0
        marker.pose.orientation.z = 0
        marker.pose.orientation.w = 1

        marker.scale.x = 1
        marker.scale.y = 1
        marker.scale.z = 1

        marker.color.r = self.color[0]
        marker.color.g = self.color[1]
        marker.color.b = self.color[2]
        marker.color.a = self.color[3]

        marker.lifetime = rospy.Duration.from_sec(1 / rospy.get_param('~pub_rate'))
        marker.frame_locked = False

        print(self.name)
        print("points: " + str(self.points) + "\n")
        self.triangled_points = pytess.triangulate(self.points)
        print("triangled_points: " + str(self.triangled_points) + "\n")

        for triangle in self.triangled_points:
            for point in triangle:
                p = Point()
                p.x = point[0]
                p.y = point[1]
                p.z = 0.01
                marker.points.append(p)
                marker.colors.append(marker.color)
        return marker


def get_rooms(urdf):
    room_joints = []
    rooms = []
    joints = urdf.joints
    room_parser = re.compile('world_\w+_room_joint')
    for j in joints:
        if room_parser.match(j.name):
            room_joints.append(j)
            #joints.remove(j)

    for room_joint in room_joints:
        room = Room()
        room.name = room_joint.name[6:len(room_joint.name) - 11]
        for link in urdf.links:
            if link.name == room_joint.child:
                room.set_color(link.visual.material.color.rgba)
        corner_parser = re.compile(room.name + '_room_joint_[0-9]+')  # {name}_room_joint_${loop_number}
        for corner_joint in joints:
            if corner_parser.match(corner_joint.name):
                print(corner_joint.name)
                room.add_point(corner_joint.origin.xyz)
                print(corner_joint.origin.xyz)
                # joints.remove(corner_joint)
        rooms.append(room)
    return rooms


def loop():
    rospy.init_node('suturo_room_viz', anonymous=True)
    pub = rospy.Publisher('room_marker_array', MarkerArray, queue_size=10)
    urdf = URDF.from_parameter_server(rospy.get_param('~urdf_param'))
    if not pytess_installed:
        rospy.logerr("PYTESS NOT INSTALLED: Rooms will not be visualized. 'sudo -H pip install pytess'")
        return
    rate = rospy.Rate(rospy.get_param('~pub_rate'))
    seq = 0
    while not rospy.is_shutdown():
        ma = MarkerArray()
        for r in get_rooms(urdf):
            ma.markers.append(r.to_marker(seq))
            seq += 1
        print(seq)

        pub.publish(ma)
        rate.sleep()


if __name__ == '__main__':
    try:
        loop()
    except rospy.ROSInterruptException:
        pass
