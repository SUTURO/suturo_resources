#!/bin/bash

# ROS Noetic Installer Script
# This script installs ROS Noetic Desktop Full on Ubuntu 20.04

# Exit immediately if any command fails
set -e

# Check if running on Ubuntu 20.04
if [[ $(lsb_release -sc) != "focal" ]]; then
    echo "This script is only for Ubuntu 20.04 (Focal Fossa)"
    exit 1
fi

echo "Starting ROS Noetic Desktop Full installation..."

# 1. Configure repositories
echo "Adding ROS repository..."
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'

# 2. Set up keys
echo "Setting up keys..."
sudo apt install curl -y
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -

# 3. Update package index
echo "Updating package list..."
sudo apt update -y

# 4. Install ROS Noetic Desktop Full
echo "Installing ROS Noetic Desktop Full (this may take a while)..."
sudo apt install ros-noetic-desktop-full -y

# 5. Initialize rosdep
echo "Initializing rosdep..."
sudo rosdep init
rosdep update

# 6. Add ROS to bashrc
echo "Sourcing ROS in .bashrc..."
echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
# 7. Install additional dependencies
echo "Installing build tools and dependencies..."
sudo apt install python3-rosinstall python3-rosinstall-generator python3-wstool build-essential -y

echo ""
echo "ROS Noetic Desktop Full installation complete!"
echo "Now source 'source ~/.bashrc' and everything should be working"
echo "To test your installation, try running:"
echo "roscore"
