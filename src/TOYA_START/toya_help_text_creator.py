#!/usr/bin/env python3

"""
This program is a simple text formatter designed to enhance a plain text help file by combining it with an ASCII
art image. It reads a .txt file line by line and formats the output so that an ASCII artwork appears on the left
side of the terminal, while explanatory text is displayed on the right side.

Because the program processes the text strictly as individual lines (without automatic line wrapping), it is important
to ensure that each line of text is not too long. If the lines exceed the available terminal width, the output may
become unreadable or be cut off. Therefore, the text should be manually formatted with appropriate line lengths before
processing.

The input help text is stored in the file help_text.txt. After formatting, the resulting output—which includes both the
ASCII artwork and the aligned text—is written to help_text_with_image.txt. This output file can then be displayed in the
terminal to present a visually structured and more engaging help message.
"""


picture = open('toya.txt', 'r')

text = open('help_text.txt', 'r')

created_text = open('help_text_with_image.txt', 'w')

lines_toya = picture.readlines()
lines_text = text.readlines()

output = ""

for i in range (0, (max(len(lines_toya), len(lines_text)))):
    if(i >= len(lines_toya)):
        output += lines_text[i]
    elif(i >= len(lines_text)):
        output += lines_toya[i]
    else:
        output = output + lines_toya[i].replace("\n", "") + "        " + lines_text[i]

output = output + "\n" + "\n"
output += "#############################################################################################################################"
output = output + "\n" + "Activate Virtual Environments:		PATH/bin/activate" + "\n" + "or for some:				WORKON x" + "\n"
output += "---------------------------------------------------------\n"

created_text.write(output)
