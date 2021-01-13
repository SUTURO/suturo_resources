nlg_msgs/KeyValuePair[] role_values

#Filled with some key value pairs representing a sentence e.g.
# [["action","place"],["object_id","redpringlescan_ABCDEF"],["surface_id","bookshelf_0_shelf_1"]]
# Results in a sentence like: "I will place the red pringles can in the middle of the bookshelf"

# [["cantmove", "too small"],["object_id","redpringlescan_ABCDEF"]]
# Results in a sentence like: "I cant move the red pringles can it is to small"


# "move" can be used with goal_room, goal_surface AND goal_object
# resulting in "I am moving to the red pringles can on the table in the living room"
# but can be used with any number of goals

# The order of Key Value pairs inside the array is not important.
# KVPs should result in single sentences. Be aware that some combinations might not make sence and throw errors.
# When using knowledge ids and they are not found in knowledge the string is directly placed in the textgen. 
