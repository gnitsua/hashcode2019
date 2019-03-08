from Parser import Parser


class SimpleDataset():
    """
    This is a special class as a placeholder for Dataset() that has been created in another branch
    """

    def __init__(self, dataset_letter):
        self.dataset_letter = dataset_letter
        self.images = Parser.parse(self.dataset_letter)
