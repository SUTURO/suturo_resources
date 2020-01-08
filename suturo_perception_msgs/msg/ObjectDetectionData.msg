# Communicated via actionserver at topic /perception_actionserver/result

string name
float64 confidence
uint32 shape # and the shape (please, if possible, as fallback if confidence is low). 
geometry_msgs/PoseStamped pose
float64 width
float64 height
float64 depth
std_msgs/ColorRGBA color
geometry_msgs/TransformStamped relative_tf_tree

# Shape values
uint32 MISC=0
uint32 BOX=1
uint32 CYLINDER=2
uint32 SPHERE=3
uint32 CONE=4
uint32 PLANE=5
