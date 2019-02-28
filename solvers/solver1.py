from BaseSolver import Solver
from slideshow import SlideShow
from constants import Orientation

class Solver1(Solver):
    def solve(self):
        slideshow = SlideShow()

        for i in range(len(self.dataset)):
            image = self.dataset[-i]
            if image.orientation == Orientation.vertical:
                continue

            slideshow.add_slide(image, None)

        # image_hash = ImageHash(self.dataset)
        # # image_hash.hash_images()

        # # Pick random first image
        # current_image = image_hash.get_random_image()

        # slideshow.add_slide(current_image, None)

        # # Pick the rest of the slides
        # while image_hash.len > 0:
        #     tags = current_image.tags

        #     next_image = image_hash.get_random_image()
        #     next_key = None
            # next_key = image_hash.get_potential_next(tags)
            # if next_key:
            #     next_image = image_hash.get_image(next_key)
            # else:
            #     next_image = image_hash.get_random_image()

            # if next_image.orientation == Orientation.vertical:
            #     i2 = image_hash.get_random_image()

            # else:
            #     i2 = None

            # print next_image.orientation, i2 and i2.orientation
            # slideshow.add_slide(next_image, None)

            # current_image = next_image
            # current_key = next_key

        return slideshow

class ImageHash():
    def __init__(self, images):
        self.images = images
        self.len = len(images)
        self.hash = self.hash_images()

    # def hash_images(self):
    #     image_hash = {}
    #     count = 0

    #     for image in self.images:
    #         if image.orientation == Orientation.vertical:
    #             continue
    #         else:
    #             count += 1
    #         key = '-'.join(sorted(list(image.tags)))
    #         image_hash[key] = image_hash.get(key, []) + [image]

    #     self.hash = image_hash
    #     self.len = count

    #     return image_hash

    def keys(self):
        return set(self.hash.keys())

    def get_image(self, key):
        # Return an image with that hash, removing from list
        # of available images and decrementing numner of images available
        self.len -= 1

        # remove element from list
        image = self.hash[key].pop()

        # if list is now empty, remove key from hash
        if self.hash[key] == []:
            self.hash.pop(key)

        return image

    def get_random_image(self):
        random_key = self.keys().pop()
        return self.get_image(random_key)

    def get_potential_next(self, tags):
        # Return keys that contain at least one of the provided tags
        keys = self.keys()

        for tag in tags:
            for key in keys:
                if tag in key:
                    return key

        return None
