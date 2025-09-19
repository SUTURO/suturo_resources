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

source ~/dummy/deps_ws/devel/setup.bash

echo "Starting NLP workspace setup"

# 1. Create ws directories
echo "Creating needed directories"
mkdir -p ./dummy/nlp_ws/src

# 2. Clone repos
echo "Cloning relevant repositories"
cd ./dummy/nlp_ws/src
git clone git@github.com:SUTURO/suturo_nlp.git
git clone git@github.com:SUTURO/suturo_rasa.git

# 3. Build workspace
echo "Building the workspace"
cd ..
catkin init
catkin profile add nlp_ws
catkin profile set nlp_ws
catkin config --init
catkin config --extend ~/ros/deps_ws/devel
catkin build

echo "Building of the NLP workspace complete!"
