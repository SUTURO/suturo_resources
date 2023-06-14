cmake_minimum_required(VERSION 2.8.3)
project(suturo_bringup)

find_package(catkin REQUIRED COMPONENTS
  suturo_resources
  hsr_description
  map_server
  xacro
  tf2_ros
)

catkin_package()
