cmake_minimum_required(VERSION 2.8.3)
project(suturo_resources)

find_package(catkin REQUIRED COMPONENTS

)

catkin_package()

install(DIRECTORY
  models
  maps
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
)
