cmake_minimum_required(VERSION 2.8.3)
project(navigation_msgs)

set(MSG_DEPS
  std_msgs
  geometry_msgs
  message_generation
)

find_package(catkin REQUIRED COMPONENTS
  std_msgs
  geometry_msgs
  message_generation
)

add_message_files(
  DIRECTORY msg
  FILES
  Area.msg
)


generate_messages(DEPENDENCIES
  std_msgs
  geometry_msgs
)

catkin_package(DEPENDS ${MSG_DEPS} message_runtime)
