cmake_minimum_required(VERSION 2.8.3)
project(perception_msgs)

if(NOT CMAKE_CONFIGURATION_TYPES AND NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

set(MSG_DEPS
  std_msgs
)

find_package(catkin REQUIRED COMPONENTS
  ${MSG_DEPS}
  message_generation
)

add_message_files(
   FILES
   RSObjectDescriptions.msg
)
generate_messages(DEPENDENCIES ${MSG_DEPS})

catkin_package(DEPENDS ${MSG_DEPS} message_runtime actionlib)
