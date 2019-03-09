import random

from Parser import Parser

random.seed()


class Dataset():
    def __init__(self, dataset_letter):
        self.dataset_letter = dataset_letter
        self.images = Parser.parse(dataset_letter)

    def get(self, safeness=1):
        """
        Get a random member of the dataset
        :param safeness doesn't actually do anything here, gets from a Dataset are always safe #TODO: what is the better way to do this?
        :rtype: Image
        :return: random Image() from dataset
        """
        random_image_number = random.randint(0, len(self.images) - 1)
        return self.images[int(random_image_number)]
