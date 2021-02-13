cmake_minimum_required(VERSION 2.8 FATAL_ERROR)
project(suturo_gz_text_renderer)

if(POLICY CMP0100)
  cmake_policy(SET CMP0100 NEW)
endif()

set (CMAKE_AUTOMOC ON)

find_package (Qt5Widgets REQUIRED)
find_package (Qt5Core REQUIRED)
find_package(Protobuf REQUIRED)
find_package(gazebo REQUIRED)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
  gazebo_ros
)
find_package(gazebo REQUIRED)
find_package (Qt5Widgets REQUIRED)
find_package (Qt5Core REQUIRED)
find_package(Protobuf REQUIRED)
find_package(gazebo REQUIRED)

link_directories(${GAZEBO_LIBRARY_DIRS} )
include_directories(${Boost_INCLUDE_DIR} ${catkin_INCLUDE_DIRS} ${GAZEBO_INCLUDE_DIRS} ${Qt5Core_INCLUDE_DIRS})

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${GAZEBO_CXX_FLAGS}")

catkin_package(
  DEPENDS
    roscpp
    gazebo_ros
)

add_library(suturo_gz_text_renderer SHARED ${headers_MOC} src/SRW.cc)
target_link_libraries(suturo_gz_text_renderer ${GAZEBO_LIBRARIES}
    ${OGRE_LIBRARIES}
    ${OGRE-Terrain_LIBRARIES}
    ${Qt5Core_LIBRARIES}
    ${Qt5Widgets_LIBRARIES}
    ${PROTOBUF_LIBRARIES})
