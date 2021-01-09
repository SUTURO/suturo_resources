suturo_nlg/KeyValuePair[] role_values

#Filled with some key value pairs representing a sentence e.g.
# [["action","place"],["object_id","redpringlescan_ABCDEF"],["surface_id","bookshelf_0_shelf_1"]]
# Results in a sentence like: "I will place the red pringles can in the middle of the bookshelf"

# [["cantmove", "too small"],["object_id","redpringlescan_ABCDEF"]]
# Results in a sentence like: "I cant move the red pringles can it is to small"

# The order of Key Value pairs inside the array is not important.
# KVPs should result in single sentences. Be aware that some combinations might not make sence and throw errors.
