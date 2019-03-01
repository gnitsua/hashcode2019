from BaseSolver import Solver
from slideshow import SlideShow
from constants import Orientation

class Solver3(Solver):
    def solve(self):
        slideshow = SlideShow()

        image_hash = ImageHash(self.dataset)
        image_hash.hash_images()

        # Pick random first image
        current_image = image_hash.get_random_image()

        slideshow.add_images(current_image)

        # Pick the rest of the slides
        while image_hash.len > 0:
            tags = current_image.tags

            next_key = image_hash.get_potential_next(tags)
            if next_key:
                next_image = image_hash.get_image(next_key)
            else:
                next_image = image_hash.get_random_image()

            if next_image is None:  # Hack for inability to count
                break

            slideshow.add_images(next_image)

            current_image = next_image
            current_key = next_key

        return slideshow

class ImageHash():
    def __init__(self, images):
        self.images = images
        self.len = len(images)
        self.hash = self.hash_images()

    def hash_images(self):
        image_hash = {}
        limit = 10000
        count = 0

        for image in self.images:
            # Limit to only horizontal (1 per page)
            if image.orientation != Orientation.horizontal:
                continue

            # Limit the number of images being used
            if count >= limit:
                break

            key = '-'.join(sorted(list(image.tags)))
            image_hash[key] = image_hash.get(key, []) + [image]

            count += 1

        self.hash = image_hash

        return image_hash

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
        keys = self.keys()

        if keys:
            random_key = keys.pop()
            image = self.get_image(random_key)
        else:
            image = None

        return image

    def get_potential_next(self, tags):
        # Return keys that contain at least one of the provided tags
        keys = self.keys()

        for tag in tags:
            for key in keys:
                if tag in key:
                    return key

        return None
