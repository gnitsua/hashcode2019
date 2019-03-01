from BaseSolver import Solver
from slideshow import SlideShow
from constants import Orientation

class Solver1(Solver):
    """
    Creating a slide show using only vertical images and ignoring tags
    """

    def solve(self):
        slideshow = SlideShow()
        vertical_image = None

        for image in self.dataset:
            if image.orientation == Orientation.vertical:
                if vertical_image is None:
                    # Save image and wait for another vertical one
                    vertical_image = image
                else:
                    # Add both vertical images to our slideshow
                    slideshow.add_images(image, vertical_image)
                    vertical_image = None
            else:
                # Horizontal images, one per page
                slideshow.add_images(image)

        return slideshow
