from constants import Orientation

class Slide():
    def __init__(self, image1, image2):
        assert(image1 != None)
        self.image1 = image1
        self.image2 = image2
        if (self.image2 != None):
            if (self.image1.orientation == Orientation.vertical and self.image2.orientation == Orientation.vertical):
                pass
            else:
                raise AttributeError("Invalid slide configuration")

    @property
    def tags(self):
        result = self.image1.tags
        if(self.image2 != None):
            result = result | self.image2.tags
        return  result

    def __sub__(self, other):
        common_tags = self.tags.intersection(other.tags)
        tags_only_in_1 = self.tags.difference(other.tags)
        tags_only_in_2 = other.tags.difference(self.tags)
        return min(common_tags,tags_only_in_1,tags_only_in_2)

    def __str__(self):
        return "Slide ("+str(self.image1)+","+str(self.image2)+")"
