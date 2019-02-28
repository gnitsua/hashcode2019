from BaseSolver import Solver
from slideshow import SlideShow

class Solver1(Solver):
    def solve():
        slide_show = SlideShow()

        image_hash = self.hash_images()

        # Pick random first image
        image = image_hash.keys()[0]

        slideshow.add_slide(image)


        pass

    def hash_images(self):
        images = self.dataset
        image_hash = {}

        for image in images:
            key = '-'.join(sorted(list(image.tags)))
            image_hash[key] = image_hash.get(key, []) + [image]

        return image_hash