import uuid

import redis
from sortedcollections import OrderedSet

from Dataset import Dataset
from Slide import Slide
from constants import UNASSIGNED_IMAGE


class SlideShow():
    def __init__(self, dataset_letter, id=None):
        self.dataset_letter = dataset_letter
        if (id != None):
            self.id = id
        else:
            self.id = "ss" + str(uuid.uuid4())

        self.internal_score = 0
        self.slides = OrderedSet()

    @classmethod
    def fromString(cls, id, inputString, dataset):
        result = cls(dataset.dataset_letter, id)
        for line in inputString.splitlines():
            result.add_slide(Slide.fromString(line, dataset))

    @classmethod
    def getFromRedis(cls, id, dataset):
        r = redis.Redis(host="192.168.99.100")
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

    def finalize(self):
        # since the slides have all been added we can assume that it is valid by the rules
        # so let's just check if it is valid based on the redis state
        r = redis.Redis(host="192.168.99.100")
        score = self.get_score()
        slide_shows_that_would_need_to_die = set()
        for slide in self.slides:
            for image in slide:
                currently_assigned_to = r.get(image.__hash__())
                print(image.__hash__(), currently_assigned_to)
                assert (currently_assigned_to != None)  # again we are hoping that images are never not in the database
                if (currently_assigned_to == UNASSIGNED_IMAGE):
                    pass  # this is a valid image to have in this slideshow
                elif (currently_assigned_to == self.id):
                    pass  # if we are working inside
                else:
                    # slide show that would need to be deleted to allow this one to be valid
                    slide_shows_that_would_need_to_die.add(currently_assigned_to)

        print("Slideshows that would need to die" + str(slide_shows_that_would_need_to_die))

        for slide_show_that_would_need_to_die in slide_shows_that_would_need_to_die:
            slide_show_score = r.zscore(Dataset.get_dataset_score_container_key(self.dataset_letter),
                                        slide_show_that_would_need_to_die)
            # this would only happen if the slideshow was deleted between the last check and this?
            assert (slide_show_score != None)
            if (slide_show_score > score):
                raise AttributeError("another slide show is using this slide (and has a higher score)")
            else:
                pass  # this slide show will have a higher score than that one, so we can delete that one (but not yet, make sure the others are valid first)

        # if we have made it this far, the slideshow is valid, time to post it
        print("it's valid")

        # TODO: lock through this section
        # add this slideshow's score to the scoreboard
        print("Adding: " + Dataset.get_dataset_score_container_key(self.dataset_letter) + "," + self.id + "=" + str(
            score))
        r.zadd(Dataset.get_dataset_score_container_key(self.dataset_letter), {self.id: score})
        # set the lock for all of the images to this slideshow
        for slide in self.slides:
            for image in slide:
                print(str(image.__hash__()) + "=" + str(self.id))
                r.set(image.__hash__(), self.id)

        # and kill the competeing slideshows
        for slide_show_to_kill in slide_shows_that_would_need_to_die:
            print("Removing: " + slide_show_to_kill)
            r.zrem(Dataset.get_dataset_score_container_key(self.dataset_letter), slide_show_to_kill)

        # finally broadcast the slide show so others can find it
        r.set(self.id, self.__str__())

    def __str__(self):
        result = str(len(self.slides)) + "\n"
        for slide in self.slides:
            result += str(slide.image1.id) + " "
            if (slide.image2 != None):
                result += str(slide.image2.id)
            result += "\n"
        return result
