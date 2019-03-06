import uuid

import redis
from sortedcollections import OrderedSet

from Slide import Slide
from constants import REDIS_HOST
from constants import REDIS_PASWORD
from constants import UNASSIGNED_IMAGE, RedisKey


class SlideShow():
    def __init__(self, dataset_letter, id=None):
        self.dataset_letter = dataset_letter
        if (id != None):
            self.id = id
        else:
            self.id = str(uuid.uuid4())

        self.internal_score = 0
        self.slides = OrderedSet()

    @classmethod
    def fromString(cls, id, inputString, dataset):
        result = cls(dataset.dataset_letter, id)
        for line in inputString.splitlines():
            result.add_slide(Slide.fromString(line, dataset))

    @classmethod
    def getFromRedis(cls, id, dataset):
        r = redis.Redis(host=REDIS_HOST, password=REDIS_PASWORD)
        ss = r.get(id)
        if (ss != None):
            raise KeyError("Slide show not found")
        else:
            return SlideShow.fromString(id, ss,
                                        dataset)  # TODO: we could skip the score calculation if we use the one from the scoreboard

    def get_score(self):
        return self.internal_score

    def add_images(self, *args):
        slide = Slide(*args)
        self.add_slide(slide)

    def add_slide(self, slide):
        num_slides = len(self.slides)
        self.slides.add(slide)
        if (len(self.slides) != num_slides + 1):
            raise (AttributeError("slide already in slideshow"))
        else:
            if (len(self.slides) > 1):
                self.internal_score += self.slides[-1] - self.slides[-2]

    def pop(self):
        self.internal_score -= self.slides[-1] - self.slides[-2]
        self.slides.remove(max(self.slides))

    def get_images(self):
        result = []
        for slide in self.slides:
            for image in slide:
                result.append(image)
        return result

    def get_image_ids(self):
        return map(lambda image: image.__hash__(), self.get_images())

    def __str__(self):
        result = str(len(self.slides)) + "\n"
        for slide in self.slides:
            result += str(slide.image1.id) + " "
            if (slide.image2 != None):
                result += str(slide.image2.id)
            result += "\n"
        return result
