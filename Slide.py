from constants import Orientation
from image import Image


class Slide():
    def __init__(self, image1, image2=None):
        assert (image1 != None)
        self.image1 = image1
        self.image2 = image2
        if (self.image2 != None):
            if (self.image1 == self.image2):
                raise AttributeError("Invalid slide configuration")
            if (self.image1.orientation == Orientation.vertical and self.image2.orientation == Orientation.vertical):
                pass
            else:
                raise AttributeError("Invalid slide configuration")
        else:
            if (self.image1.orientation == Orientation.vertical):
                raise AttributeError("Vertical images must be in pairs")

    @classmethod
    def fromString(cls, string, dataset):
        images = []
        for image in string.rstrip().split(" "):
            images.append(Image.fromString(image, dataset))
        if (len(images) == 2):
            return Slide(images[0], images[1])
        elif (len(images) == 1):
            return Slide(images[0])
        else:
            raise AssertionError("not the right number of slides")

    @property
    def tags(self):
        result = self.image1.tags
        if (self.image2 != None):
            result = result | self.image2.tags
        return result

    def __sub__(self, other):
        common_tags = len(self.tags.intersection(other.tags))
        tags_only_in_1 = len(self.tags) - common_tags
        tags_only_in_2 = len(other.tags) - common_tags
        return min(common_tags, tags_only_in_1, tags_only_in_2)

    def __str__(self, pretty=False):
        if (pretty == True):
            return "Slide (" + str(self.image1) + "," + str(self.image2) + ")"
        else:
            return " ".join(map(str, list(self.__iter__())))  # TODO: this is ugl

    def __eq__(self, other):
        if (self.image1.id != other.image1.id):  # TODO: only checking the first image
            return False
        return True

    def __hash__(self):
        if (self.image2 != None):
            return hash((self.image1, self.image2))  # TODO: only checking the first one
        else:
            return hash(self.image1)

    def __iter__(self):
        result = [self.image1]
        if (self.image2):
            result.append(self.image2)
        return result.__iter__()
