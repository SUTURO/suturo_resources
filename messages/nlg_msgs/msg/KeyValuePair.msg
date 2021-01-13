string key
string value

# Possible Keys     | Value to use                      | Meaning
# goal_room_id      | room_id used by Knowledge         | robot has to/wants to move here/bring object here
# start_room_id     | room_id used by Knowledge         | robot gets object from here/leaves this room
# object_id         | object_id used by Knowledge       | for the object the robot wants to grap/move/cant grap etc.
# object_id_2       | object_id used by Knowledge       | when placing an object near object2 or object2 is in the way of grabbing object
# goal_surface_id   | surface_id used by Knowledge      | used for when the robot is moving to a table or placing an object on a shelffloor
# start_surface_id  | surface_id used by Knowledge      | used for when the robot grapping an object from here
# action            | "place", "pick up", "move",       | what is the robot doing
#                   | "look at"                         | needs goal_surface_id
# cantmove          | "reach", "too small", "too big"   | when the robot cant move something (should not be used in combination with action)
                    | "grab"                            | grab can be used in combination with object_id_2 or goal_surface_id if that is in the way


# When using knowledge ids and they are not found in knowledge the string is directly placed in the textgen. 

