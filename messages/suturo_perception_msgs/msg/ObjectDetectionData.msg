# Communicated via actionserver at topic /perception_actionserver/result

string name
string obj_class
float64 confidence_class

uint8 shape # and the shape (please, if possible, as fallback if confidence is low). 
float64 confidence_shape

geometry_msgs/PoseStamped pose
float64 width
float64 height
float64 depth

std_msgs/ColorRGBA color
float64 confidence_color

string region

# Shape values
uint8 ARROW=0 # Not used
uint8 CUBE=1
uint8 SPHERE=2
uint8 CYLINDER=3
