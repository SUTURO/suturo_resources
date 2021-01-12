string key
string value

# Possible Keys     | Value to use                      | Meaning
# goal_room_id      | room_id used by Knowledge         | robot has to/wants to move here/bring object here
# start_room_id     | room_id used by Knowledge         | robot gets object from here/leaves this room
# object_id         | object_id used by Knowledge       | for the object the robot wants to grap/move/cant grap etc.
# goal_surface_id   | surface_id used by Knowledge      | used for when the robot is moving to a table or placing an object on a shelffloor
# start_surface_id  | surface_id used by Knowledge      | used for when the robot grapping an object from here
# action            | "place", "pickup", "moving to",   | what is the robot doing
#                   | "looking_at"                      |
# cantmove          | "reach", "too small", "too big"   | when the robot cant move something

