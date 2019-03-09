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

    def __init__(self, raw_text):
        self.raw_text = raw_text

    def solve(self):
        slide_list = []
        used_images = ''

        slideshow = SlideShow()

        images, text = parse_string(self.raw_text)
        regexer = Regexer(text)

        # Use the first horizontal image as first page
        index = regexer.get_horizontal()[0]
        image = images[index]
        tags = image.tags
        used_images += str(index)
        slideshow.add_images(image)

        while True:
            # Try to find an image with tag
            regexer.get_image_with_tag(tags, used_images)

        return slideshow



# Utility functions
def parse_string(orig):
    # Cleans raw file format and gets it ready for processing
    lines = orig.split('\n')
    images = []
    formatted_lines = []

    for line_no, line in enumerate(lines):
        if line_no == 0 or line_no == len(lines) - 1:
            # First line is count of images
            # Last line is empty
            continue

        id = line_no - 1
        orientation, _, tags = Parser.parse_line(line)

        image = Image(id, orientation, tags)
        formatted_line = '{} o:{} {}'.format(id, orientation, '-'.join(tags))
        formatted_lines.append(formatted_line)

    formatted_string = '\n'.join(formatted_lines)

    return images, formatted_string


class Regexer():
    def __init__(self, text):
        self.text = text

    def get_horizontal(self):
        matches = re.findall(r'(\d*) o:H .+', self.text)
        return matches

    def get_image_with_tag(self, tags, used_images):
        exclude_images = '[{}]'.format(used_images)