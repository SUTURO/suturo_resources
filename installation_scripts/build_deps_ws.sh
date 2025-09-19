#!/bin/bash

# ROS Noetic Installer Script
# This script installs ROS Noetic Desktop Full on Ubuntu 20.04

# Exit immediately if any command fails
set -e

# Check if running as root
if [[ $EUID -eq 0 ]]; then
    echo "This script should not be run as root" 
    exit 1
fi

echo "Starting dependency workspace setup"

# 1. Configure repositories
echo "Creating needed directories"
mkdir -p ./dummy/deps_ws/src

# 2. Set up keys
echo "Cloning relevant repositories"
cd ./dummy/deps_ws/src
git clone git@github.com:SUTURO/suturo_resources.git
git clone git@github.com:SUTURO/hsr_description.git
git clone git@github.com:ros/std_msgs.git

# 3. Update package index
echo "Installation of the HSR simulator"
sudo sh -c 'echo "deb [arch=amd64] https://hsr-user:jD3k4G2e@packages.hsr.io/ros/ubuntu `lsb_release -cs` main" > /etc/apt/sources.list.d/tmc.list'
sudo sh -c 'echo "deb [arch=amd64] https://hsr-user:jD3k4G2e@packages.hsr.io/tmc/ubuntu `lsb_release -cs` multiverse main" >> /etc/apt/sources.list.d/tmc.list'
sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
wget https://hsr-user:jD3k4G2e@packages.hsr.io/tmc.key -O - | sudo apt-key add -
wget https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc -O - | sudo apt-key add -
wget https://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
sudo sh -c 'mkdir -p /etc/apt/auth.conf.d'
sudo sh -c '/bin/echo -e "Package: ros-noetic-laser-ortho-projector\nPin: version 0.3.3*\nPin-Priority: 1001\n\nPackage: ros-noetic-laser-scan-matcher\nPin: version 0.3.3*\nPin-Priority: 1001\n\nPackage: ros-noetic-laser-scan-sparsifier\nPin: version 0.3.3*\nPin-Priority: 1001\n\nPackage: ros-noetic-laser-scan-splitter\nPin: version 0.3.3*\nPin-Priority: 1001\n\nPackage: ros-noetic-ncd-parser\nPin: version 0.3.3*\nPin-Priority: 1001\n\nPackage: ros-noetic-polar-scan-matcher\nPin: version 0.3.3*\nPin-Priority: 1001\n\nPackage: ros-noetic-scan-to-cloud-converter\nPin: version 0.3.3*\nPin-Priority: 1001\n\nPackage: ros-noetic-scan-tools\nPin: version 0.3.3*\nPin-Priority: 1001" > /etc/apt/preferences'
sudo apt-get update
sudo apt-get install ros-noetic-tmc-desktop-full

# 4. Install additional dependencies
echo "Building the workspace"
cd ..
catkin init
catkin profile add deps_ws
catkin profile set deps_ws
catkin config --init
catkin config --extend /opt/ros/noetic
catkin build

echo "Building of the dependency workspace complete!"
