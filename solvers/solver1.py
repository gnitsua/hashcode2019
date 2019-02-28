from BaseSolver import Solver
from slideshow import SlideShow
from constants import Orientation

class Solver1(Solver):
    """
    Creating a slide show using only vertical images and ignoring tags
    """

    def solve(self):
        slideshow = SlideShow()

        for image in self.dataset:
            if image.orientation == Orientation.vertical:
                continue

            slideshow.add_slide(image, None)

        return slideshow
