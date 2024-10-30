# SETUP
```
git clone --recurse-submodules https://github.com/sunava/hsrb_rosnav # into your ROS workspace
sudo apt install ros-noetic-map-server
sudo apt-get install ros-noetic-dwa-local-planner

```
You will need this for navigation and map.

```
roslaunch suturo_bringup envi_bringup.launch
```
Note: You do not need iai_hsr pkg currently 

# suturo_resources
Repository for shared resources like world descriptions etc.

## SUTURO_BRINGUP
Suturo_bringup contains launchfiles to start the simulation.

## SUTURO_RESOURCES
This package contains map files, gazebo_worlds and URDF files.

## SUTURO_ROOM_VIZ
This package contains a node publishing a Visualisation_Marker_Array that colors the floor of each room based on TF data published by suturo_bringup.
