"""
For each dataset, orders the tags for each line, sorts the
lines by number of tags and saves the result in a new directory.

Point value of a line is dependent on the number of tags and
the orientation of the image.
    vertical = number_of_tags
    horizontal = number_of_tags / 2  # because 2 per page

This way, when we grab photos, they are most likely to have a
similar number of tags.
"""

from Parser import Parser
from constants import FilePath, Orientation, InputFile
import os

def sort_files(letters):
    for letter in letters:
        sort_file(letter)

def sort_file(letter):
    data_set_map = Parser.get_data_sets()

    input_path = data_set_map[letter]

    print 'Opening', input_path
    file = open(input_path, 'r')

    lines = []
    for line_no, line in enumerate(file):
        if line_no < InputFile.lines_to_skip:
            # Don't modify, just copy over
            lines.append((-1, line))
            continue

        _, orientation, tag_count, tags = Parser.parse_line(0, line)

        weight = tag_count if orientation == Orientation.horizontal else tag_count / 2
        tags.sort()
        line = Parser.reconstruct_line(orientation, tag_count, tags)

        lines.append((weight, line))

    lines.sort(key=lambda l: l[0])  # sort by weight

    output_path = FilePath.pwd + FilePath.sorted_data + os.path.basename(file.name)
    file.close()

    print 'Writing to', output_path
    file = open(output_path, 'w')
    for line in lines:
        file.write(line[1])  # only write original line
    file.close()

sort_files(['a', 'b', 'c', 'd', 'e'])