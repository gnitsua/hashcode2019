import random
import time

from BaseSolver import Solver
from Slide import Slide
from constants import Orientation
from slideshow import SlideShow


class Solver1(Solver):
    """
    Creating a slide show using only vertical images and ignoring tags
    """
    known_horiontal = []

    def solve(self):
        slideshow = SlideShow(self.dataset.dataset_letter)

        # unsused_images = self.dataset.images[:]
        start = time.time()
        while (time.time() - start < 10):
            try:
                random_image = self.dataset.get(0.99)
                if random_image.orientation == Orientation.vertical:
                    if (len(self.known_horiontal) > 0):

                        slideshow.add_slide(Slide(random_image, self.known_horiontal.pop(0)))

                    else:
                        self.known_horiontal.append(random_image)

                else:
                    slideshow.add_slide(Slide(random_image))
            except AttributeError as e:
                pass
                # print(e)


        self.validate(slideshow)
        return slideshow
