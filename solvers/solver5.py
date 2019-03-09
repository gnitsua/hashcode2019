from BaseSolver import Solver
from slideshow import SlideShow
from Slide import Slide
from constants import Orientation
from Parser import Parser
from image import Image
import re


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

        # Use the first horizontal image as first page
        line = regexer.get_line(Orientation.horizontal)

        image = self.get_and_use_image(line)
        tags = image.tags

        slide = Slide(image)
        slideshow.add_slide(slide)

        for x in range(1000):
            # Try to find an image with tag
            tags = [tags.pop()] if tags else []

            line = regexer.get_line_with_tags(tags, self.used_images)
            if line is None:
                line = regexer.get_random_line(self.used_images)
            if line is None:
                break


            image = self.get_and_use_image(line)

            images = []
            images.append(image)

            if image.orientation == Orientation.vertical:
                # Get another vertical image
                line = regexer.get_line(Orientation.vertical)
                if line is None:
                    continue
                image = self.get_and_use_image(line)
            else:
                image = None

            images.append(image)

            # Generate tags for this slide
            tags = set().union(*[i for i in images if i])

            slide = Slide(*images)
            slideshow.add_slide(slide)

        return slideshow

    def get_and_use_image(self, line):
        # Takes in a line and does all the necessary stuff
        id = Regexer.get_id(line)
        self.add_to_used_images(id)
        return self.images[int(id)]

    def add_to_used_images(self, id):
        if self.used_images:
            str = '|{}'.format(id)
        else:
            str = '{}'.format(id)

        self.used_images += str


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

        formatted_line = '{} o:{} {}'.format(id, orientation, '-'.join(tags))
        formatted_lines.append(formatted_line)

    formatted_string = ''.join(formatted_lines)

    return images, formatted_string

def get_tag_subset(tags, number_of_tags=1):
    # Returns a set number of tags, if there aren't enough tags available,
    # just return them all
    tag_list = list(tags)

    count = number_of_tags if number_of_tags <= len(tag_list) else len(tag_list)
    slice = tag_list[:count]

    return slice


class Regexer():
    ID = r'(\d*)'

    def __init__(self, text=''):
        self.text = text

    @staticmethod
    def get_id(line):
        match = re.search(Regexer.ID, line)
        return match.group()

    def get_line(self, o=None, t=None):
        id = self.ID

        if o:
            abbreviation = 'H' if o == Orientation.horizontal else 'V'
            orientation = r'o:{}'.format(abbreviation)
        else:
            orientation = r'o:.'

        if t:
            # logic for tags
            pass
        else:
            tags = r'.+'

        regex = r'{} {} {}'.format(id, orientation, tags)
        match = re.search(regex, self.text)

        return match and match.group()


    def get_random_line(self, used_lines):
        exclude_lines = r'^(?!{})'.format(used_lines)
        match = re.search(exclude_lines, self.text)

        return match and match.group()


    def get_line_with_tags(self, tags, used_lines):
        exclude_lines = r'^(?!{})'.format(used_lines)
        include_tags = ''.join(r'(?=.*{})'.format(t) for t in tags)
        regex = exclude_lines + include_tags

        match = re.search(regex, self.text)

        return match and match.group()
