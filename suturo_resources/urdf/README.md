# SUTURO URDF files
The SUTURO URDF files are used to hard code information of the enviornment/rooms/apartment. These information are used by:
 + Knowledge to know the different rooms
 + Knowledge to know where objects can be placed/found
 + Knowledge/NLG to know the names of these things
 + Perception to create Regions when perceiving
 + Manipulation/Navigation to perform collision avoidance
 + Manipulation where are doors and how can they be opened

## Naming Scheme
URDF files fall into one of these categories:
 + real world enviornment named : rw\_**.urdf.xacro
 + gazebo enviornments used by the whole team to test the full system : gz\_full\_**.urdf.xacro
 + gazebo enviornments containing only some elements / used for testing single componends : gz\_test\_**.urdf.xacro
Call the .yaml the same as the urdf file.

## urdf_components
The folder urdf\_components contains xacro files that only have the pupose to devine macros. Each macro handles the creation of one of the following things.

### Bucket

### Door

### Room

### Shelf

### Table

### Wall

## The suturo_enviornment.urdf.xacro file
This file handles the loading of the .yaml file associated with every enviornment. It then calls the different macros to create the whole urdf files.
Every other .urdf.xacro file serves the purpose of calling suturo_enviornment.urdf.xacro with a specific .yaml file.



# Creating a new Enviornment
