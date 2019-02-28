from BaseSolver import Solver

class Solver1(Solver):
    def solve():
        pass

    def hash_images(self):
        images = self.dataset
        image_hash = {}

        for image in images:
            key = '-'.join(sorted(list(image.tags)))
            image_hash[key] = image_hash.get(key, []) + [image]

        return image_hash