# Global Pose Updater
For the Carry My Luggage/Help me Carry Challenge:
This little node takes the /poseupdate topic of type PoseWithCovariancecStamped
which is published by hector_slam, and republishes the pose on the 
/global_pose topic of type PoseStamped.
The result is that now the hector_slam localization can be used and no amcl or 
pose_integrator nodes are needed, as long as hector_slam is running.

run with: 
```=python
rosrun global_pose_updater global_pose_updater.py
```
