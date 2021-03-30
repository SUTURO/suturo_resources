# SUTURO URDF files
The SUTURO URDF files are used to hard code information of the enviornment/rooms/apartment. These information are used by:
 + Knowledge to know the different rooms
 + Knowledge to know where objects can be placed/found
 + Knowledge/NLG to know the names of these things
 + Perception to create Regions when perceiving
 + Manipulation/Navigation to perform collision avoidance
 + Manipulation where are doors and how can they be opened


## Concept
The URDF system contain ~one launchfile~, ~one main urdf.xacro~ and ~six component urdf.xacro~. The information about individual rooms one only stored in ~.yaml~ files.

### The suturo_enviornment.urdf.xacro file
This file handles the loading of the .yaml file associated with every enviornment. It then calls the different macros to create the whole urdf files.
Every other .urdf.xacro file serves the purpose of calling suturo_enviornment.urdf.xacro with a specific .yaml file.


### YAML files
Each yaml file describes one enviornment the robot can be in.
yaml files fall into one of these categories:
 + real world enviornment named : ~rw\_**.yaml~
 + gazebo enviornments used by the whole team to test the full system : ~gz\_full\_**.yaml~
 + gazebo enviornments containing only some elements / used for testing single componends : ~gz\_test\_**.yaml~


### urdf_components
The folder urdf\_components contains xacro files that only have the pupose to devine macros. Each macro handles the creation of one of the following things.
 + Bucket
 + Door
 + Room
 + Shelf
 + Table
 + Wall



# Creating a new Enviornment

First follow the naming scheme (above) for your enviornment.
