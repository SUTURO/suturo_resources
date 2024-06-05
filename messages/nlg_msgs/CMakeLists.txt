cmake_minimum_required(VERSION 2.8.3)
project(nlg_msgs)

## Compile as C++11, supported in ROS Kinetic and newer
# add_compile_options(-std=c++11)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  rospy
  std_msgs
  message_generation
  actionlib
  actionlib_msgs
)



add_message_files(
   DIRECTORY msg
   FILES
   KeyValuePair.msg
)

add_action_files(
  DIRECTORY action
  FILES
  LanguageGeneration.action
)

generate_messages(
  DEPENDENCIES
  std_msgs
  actionlib_msgs
)

catkin_package(
  CATKIN_DEPENDS std_msgs
  actionlib_msgs
)


include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)



