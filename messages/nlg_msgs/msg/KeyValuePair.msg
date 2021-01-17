string key
string value

# Possible Keys     | Value to use                      | Meaning
# goal_room_id      | room_id used by Knowledge         | robot has to/wants to move here/bring object here
# start_room_id     | room_id used by Knowledge         | robot gets object from here/leaves this room
# object_id         | object_id used by Knowledge       | for the object the robot wants to grap/move/cant grap etc.
# object_id_2       | object_id used by Knowledge       | when placing an object near object2 or object2 is in the way of grabbing object
# goal_surface_id   | surface_id used by Knowledge      | used for when the robot is moving to a table or placing an object on a shelffloor
# start_surface_id  | surface_id used by Knowledge      | used for when the robot grapping an object from here
# action            | "place", "grasp", "move",         | what is the robot doing / move without object_id results in "I'm moving to..." / with object_id "I'm moving pringles can to..." / object_id_2 can beused as a thing the robot moves to
#                   | "percieve"                         | needs goal_surface_id
# reason            | "free space", "similar type",     | used with place and when not free space object_id_2
#                   |"similar color", "similar size"    |
# cantmove          | "reach", "too small", "too big"   | when the robot cant move something (should not be used in combination with action)
#                   | "grab"                            | grab can be used in combination with object_id_2 or goal_surface_id if that is in the way
# starting          | "clean up", "groceries", "safety test" | not used with anything else

# When using knowledge ids and they are not found in knowledge the string is directly placed in the textgen. 

