from constants import Orientation


class Image(object):
    def __init__(self, id, orientation, tags):
        self.id = int(id)
        self.orientation = Orientation.horizontal if orientation == 'H' else Orientation.vertical
        self.tags = set(tags)
        self.number_of_tags = len(tags)

    @classmethod
    def fromString(cls, string, dataset):
        try:
            string_as_int = int(string[2:])  # skip the "databaseletter-"
            return dataset[string_as_int]
        except ValueError as e:
            raise e
        except IndexError as e:
            raise e

    def set_database_letter(self, letter):
        self.database_letter = letter

    def __sub__(self, other):
        return self.tags - other.tags

    def __hash__(self):
        return str(self.id)

    def __str__(self):
        return "" + str(self.id) + "(" + self.orientation + "): " + str(self.tags)
