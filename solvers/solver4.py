from BaseSolver import Solver
from slideshow import SlideShow
from Slide import Slide
from constants import Orientation

class Solver4(Solver):
    """
    Creating a slide show by grouping slides (H or VV) by number of tags
    """

    def solve(self):
        slideshow = SlideShow()

        slides = []
        vertical_image = None
        for image in self.dataset:
            if image.orientation == Orientation.vertical:
                if vertical_image is None:
                    # Save image and wait for another vertical one
                    vertical_image = image
                else:
                    # Add both vertical images to a slide
                    slide = Slide(image, vertical_image)
                    tag_count = image.number_of_tags + vertical_image.number_of_tags
                    slides.append((tag_count, slide))

                    vertical_image = None
            else:
                # Horizontal images, one per slide
                slide = Slide(image)
                tag_count = image.number_of_tags
                slides.append((tag_count, slide))

        # Sort the slides by number of tags
        ordered_slides = sorted(slides, key=lambda slide: slide[0])

        # Put slides directly into slide show
        for tag_count, slide in ordered_slides:
            slideshow.add_slide(slide)

        return slideshow
