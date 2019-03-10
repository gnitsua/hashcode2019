import uuid

from Slide import Slide
from errors import ImageInSlideShowError


class SlideShow():
    def __init__(self, dataset_letter, id=None):
        self.dataset_letter = dataset_letter
        if (id == None):
            self.id = str(uuid.uuid4())
        else:
            self.id = id

        self.internal_score = 0
        self.slides = []
        self.images = set()

    @classmethod
    def fromString(cls, inputString, dataset):
        result = cls(dataset.dataset_letter)  # create a new id for this version so it can compete with the old one
        for line in inputString.splitlines()[1:]:
            result.add_slide(Slide.fromString(line, dataset))

        return result

    def get_score(self):
        return self.internal_score

    def add_images(self, *args):
        slide = Slide(*args)
        self.add_slide(slide)

    def add_slide(self, slide):
        # check if it can be added
        for image in slide:
            if image in self.images:
                raise (ImageInSlideShowError("{} already in slideshow".format(image.id)))

        # if so add
        self.slides.append(slide)
        for image in slide:
            self.images.add(image)

        if(len(self.slides) > 1):
            self.internal_score += self.slides[-1]-self.slides[-2]

    def pop(self):
        for image in self.slides[-1]:
            self.images.remove(image)
        self.internal_score -= self.slides[-1] - self.slides[-2]
        self.slides.pop(-1)

    def get_images(self):
        result = []
        for slide in self.slides:
            for image in slide:
                result.append(image)
        return result

    def get_image_ids(self):
        return map(lambda image: image.__hash__(), self.get_images())

    def save_to_file(self, filepath="results/"):
        with open(filepath + "result-" + self.dataset_letter + "-" + str(self.get_score()) + ".txt", "w") as file:
            file.write(str(self))

    def __str__(self, pretty=False):
        result = str(len(self.slides)) + "\n"
        for slide in self.slides:
            result += slide.__str__(pretty)
            result += "\n"
        return result
