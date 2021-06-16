# Send when NLP hears a command from the "Go and Get It" Task
# Sentences like: Go to the ~kitchen~ and bring me the ~cup~
#                 There is a ~red pringles can~ in the ~living room~, bring it to me please
# knowledge will have to understand these words. NLP only extracts the words, planning only passes them on
#
# strings might contain spaces. e.g. for objects like "red cup"

string perceived_object_name

bool person_left
bool person_right
