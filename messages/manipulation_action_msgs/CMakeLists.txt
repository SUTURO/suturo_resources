cmake_minimum_required(VERSION 2.8.3)
project(manipulation_action_msgs)

if(NOT CMAKE_CONFIGURATION_TYPES AND NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

set(MSG_DEPS
  std_msgs
  geometry_msgs
  actionlib_msgs
)

set(ACT_FILES
  Grasp.action
  MoveGripper.action
  Perceive.action
  Place.action
)

find_package(catkin REQUIRED COMPONENTS
  ${MSG_DEPS}
  message_generation
  actionlib
)

add_action_files(DIRECTORY action FILES ${ACT_FILES})

generate_messages(DEPENDENCIES ${MSG_DEPS})

catkin_package(DEPENDS ${MSG_DEPS} message_runtime actionlib)
