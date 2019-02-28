from constants import Orientation

class Image(object):
    def __init__(self, id, orientation, tags):
        self.id = int(id)
        self.orientation = Orientation.horizontal if orientation == 'H' else Orientation.vertical
        self.tags = set(tags)
        self.number_of_tags = len(tags)

    def __sub__(self, other):
        return self.tags-other.tags
