cmake_minimum_required(VERSION 2.8.3)
project(global_pose_updater)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  rospy
  std_msgs
)

catkin_package()

install(DIRECTORY
  models
  maps
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)

catkin_install_python(PROGRAMS
  src/global_pose_publisher.py
   src/amcl_to_global_pose.py
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)
