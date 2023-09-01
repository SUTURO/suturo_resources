cmake_minimum_required(VERSION 2.8.3)
project(manipulation_msgs)

set(MSG_DEPS
  std_msgs
  geometry_msgs
  actionlib_msgs
  message_generation
)

find_package(catkin REQUIRED COMPONENTS
  std_msgs
  geometry_msgs
  actionlib_msgs
  message_generation
  actionlib
)

add_message_files(
  DIRECTORY msg
  FILES
  ObjectInGripper.msg
  ContextAction.msg
  ContextFromAbove.msg
  ContextNeatly.msg
  ContextObjectSize.msg
  ContextObjectType.msg
  ContextObjectShape.msg
)

add_action_files(
  DIRECTORY action
  FILES
  Grasp.action
  MoveGripper.action
  TakePose.action
  Place.action
  Open.action
  MakePlan.action
)

generate_messages(DEPENDENCIES
  std_msgs
  geometry_msgs
  actionlib_msgs
)

catkin_package(DEPENDS ${MSG_DEPS} message_runtime actionlib)
