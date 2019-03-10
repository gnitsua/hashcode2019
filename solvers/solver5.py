import datetime as dt
import math
import re

from BaseSolver import Solver
from Parser import Parser
from Slide import Slide
from constants import Orientation
from image import Image
from slideshow import SlideShow



"""
TODO:
 - sort dataset by number of tags
 - pick a vertical that doesn't share tags with it's partner
 - create solution6 that leverages solution5 with multiple processes
"""

class Solver5(Solver):
    """
    Creating a slide show by grouping slides (H or VV) by number of tags
    """

    def __init__(self, lines):
        self.lines = lines
        self.raw_text = ''
        self.used_images = ''
        self.images = []

    def solve(self, letter):
        slideshow = SlideShow(letter)

        self.images, text = parse_string(self.lines)
        regexer = Regexer(text)

        tags = []

        tic = None
        for x in range(100000):
            if x % 400 == 0:
                if tic:
                    toc = dt.datetime.now()
                    print toc - tic
                tic = dt.datetime.now()
                print x, '\t',

            line = self.get_similar_line(regexer, tags)
            if line is None:
                break

            image = self.get_and_use_image(regexer, line)

            images = []
            images.append(image)

            if image.orientation == Orientation.vertical:
                # Get another vertical image
                line = regexer.get_line(o=Orientation.vertical)
                if line is None:
                    continue
                image = self.get_and_use_image(regexer, line)
            else:
                image = None

            images.append(image)
            # print images

            # Generate tags for this slide
            tags = set().union(*[i.tags for i in images if i])

            slide = Slide(*images)
            slideshow.add_slide(slide)

        return slideshow

    def get_and_use_image(self, regexer, line):
        # Takes in a line and does all the necessary stuff

        regexer.remove_line(line)

        id = Regexer.get_id(line)
        # self.add_to_used_images(id)
        return self.images[int(id)]

    def add_to_used_images(self, id):
        # Note: The space after id (ie. '{} ') is so that it only matches that number
        #       not any numbers that start with the ids
        if self.used_images:
            str = '|{} '.format(id)
        else:
            str = '{} '.format(id)

        # print self.used_images
        self.used_images += str

    def get_similar_line(self, regexer, tags):
        tag_minimum = int(math.ceil(len(tags) / 4.0))

        # Attempt to get a line with similar tags
        while tag_minimum > 0:
            line = regexer.get_line(t=tags, tm=tag_minimum)

            if line:
                # print tag_minimum, '/', int(math.ceil(len(tags) / 3.0))
                return line

            # No line found, loosen our requirements
            tag_minimum -= 1

        # Unable to find similar line, get random line
        # Or if there are no lines left, return None
        line = regexer.get_line()
        # print 'random line'
        return line

# Utility functions
def parse_string(lines):
    # Cleans raw file format and gets it ready for processing
    images = []
    formatted_lines = []

    for line_no, line in enumerate(lines):
        if line_no == 0 or line_no == len(lines) - 1:
            # First line is count of images
            # Last line is empty
            continue

        id, orientation, tags = Parser.parse_line(line_no, line)

        image = Image(id, orientation, tags)
        images.append(image)

        tags.sort()

        # Note: dash at end of tag to match regex
        formatted_line = 'id:{} o:{} -{}-'.format(id, orientation, '--'.join(tags))
        formatted_lines.append(formatted_line)

    formatted_string = '\n'.join(formatted_lines)

    return images, formatted_string


def get_tag_subset(tags, number_of_tags=None):
    # Returns a set number of tags, if there aren't enough tags available,
    # just return them all
    tag_list = list(tags)

    if number_of_tags:
        count = number_of_tags if number_of_tags <= len(tag_list) else len(tag_list)
    else:
        # Custom logic
        count = int(math.floor(len(tag_list) / 2.0))
        # count = len(tag_list)

    slice = tag_list[:count]

    return count, slice


class Regexer():
    ID = r'id:(\d*)'

    def __init__(self, text=''):
        self.text = text

    @staticmethod
    def get_id(line):
        match = re.search(Regexer.ID, line)
        return match.group(1)

    def get_line(self, i=None, o=None, t=None, tm=1):
        if i:
            id = r'id:(?!{})\d*'.format(i)
        else:
            id = r'id:\d*'

        if o:
            abbreviation = 'H' if o == Orientation.horizontal else 'V'
            orientation = r'o:{}'.format(abbreviation)
        else:
            orientation = r'o:.'

        if t:
            tag_options = r'(-{}-)'.format('-|-'.join(t))
            tags = r'.*?'.join(tm * [tag_options])
        else:
            tags = r'.+'

        regex = r'{} {} {}'.format(id, orientation, tags)
        match = re.search(regex, self.text)

        return match and match.group()

    def get_random_line(self, used_lines):
        exclude_lines = r'id:(?!{}).*'.format(used_lines)
        match = re.search(exclude_lines, self.text)

        return match and match.group()

    def get_line_with_tags(self, tags, used_lines):
        exclude_lines = r'id:(?!{})'.format(used_lines)
        include_tags = ''.join(r'(?=.*{}).*'.format(t) for t in tags)
        regex = exclude_lines + include_tags

        match = re.search(regex, self.text)

        return match and match.group()

    def remove_line(self, line):
        r = re.compile(line)
        self.text = r.sub('', self.text)
