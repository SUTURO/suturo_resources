# Suturo_urdf_publisher
This package is used to describe the enviornment the robot interacts with.
It contains doors, shelfs, tables and buckets. These objects are dynamicly generated in xacro files. They rely on .yaml files for their exact information.
Through the lauchfiles the generated urdf are put on the ROS Param Server.

## Suturo_URDF_Publisher vs. Suturo_URDF_Publisher_rework
The suturo_urdf_publisher_rework simplifies the launchfiles, the yaml and the .urdf.xacro files. It also changed the rosparameter to /enviornmet instead of /hrsb_lab. Dew to timeconstarains the suturo project does not use the rework. The rework also currently does not contain doors or baskets.
