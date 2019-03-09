import time
from random import random

from Dataset import Dataset
from Redis import Redis
from constants import RedisKey
from errors import ImageInAnotherSlideShowError
from errors import ImageInSlideShowError
from slideshow import SlideShow


class RedisDataset(object, Dataset):
    def __init__(self, dataset_letter, redis_host, redis_password, start_fresh=False):
        """
        Initializes dataset that is connected to redis
        :param dataset_letter: dataset to load
        :param redis_host: host for redis
        :param redis_password: password for redis
        :param start_fresh: whether redis should be cleared of any existing references to this dataset
        """
        Dataset.__init__(self, dataset_letter)
        self.r = Redis(redis_host, redis_password)
        if (start_fresh == True):
            self.remove()
        self.add()

    def add(self):
        self.r.add_dataset(self)

    def remove(self):
        self.r.flush_associated_keys(self.dataset_letter)

    def slide_shows(self):
        return self.r.get_all_slide_shows(self.dataset_letter)

    def get_slide_show(self, slide_show_id):
        slide_show_string = self.r.get_slide_show_string(slide_show_id, self.dataset_letter)
        try:
            ss = SlideShow.fromString(slide_show_string, self)
            ss.id = slide_show_id
            return ss
        except ImageInSlideShowError as e:
            raise AssertionError(e.message)

    def upload(self, slide_show):
        start = time.time()
        try:
            self.r.create_slide_show(slide_show.id, slide_show.get_image_ids(), slide_show.get_score(), str(slide_show),
                                     self.dataset_letter)
        except ImageInAnotherSlideShowError as e:
            temp_slide_show = self.r.create_temp_slide_show(slide_show.get_image_ids())
            slide_shows_to_kill = self.r.find_connected_components(temp_slide_show, self.dataset_letter)

            # iff the slide show has a higher score than any of the ones containing the same slides
            print("slide shows to kill {}".format(slide_shows_to_kill))
            for slide_show_to_kill in slide_shows_to_kill:
                score = self.r.get_score(self.dataset_letter, slide_show_to_kill)
                if (score > slide_show.get_score()):
                    raise ImageInAnotherSlideShowError(
                        "Image in slideshow with higher score ({} > {})".format(score, slide_show.get_score()))

            # then delete those slide shows
            for slide_show_to_kill in slide_shows_to_kill:
                self.r.remove_slide_show(slide_show_to_kill, self.dataset_letter)

            # then try to create it again
            self.r.create_slide_show(slide_show.id, slide_show.get_image_ids(), slide_show.get_score(), str(slide_show),
                                     self.dataset_letter)

    def remove_slide_show(self, slide_show_id):
        self.r.remove_slide_show(slide_show_id, self.dataset_letter)

    def scoreboard(self):
        return self.r.get_scoreboard(self.dataset_letter)

    def get_unused(self):
        return self.r.get_unused_images(self.dataset_letter)

    def get(self, safeness=1):
        """
        Get a random image from the dataset. If safeness is 0, returns a random image from images without consulting redis.
        Note: if there are no unused images, this is equivalent to calling get(0)
        :param safeness: percent chance of getting an image already in another dataset 0-1 float
        :return: Image
        """
        if (random() > safeness):
            return super(RedisDataset, self).get()  # for unsafe gets, just get from self.images
        else:
            unused_image_id = self.r.get_random_unused_image(self.dataset_letter)
            if (unused_image_id != None):
                return self.images[int(unused_image_id)]
            else:
                return super(RedisDataset,
                             self).get()  # there are no unused images, but we still need to return something

    def intersect(self, slide_show):
        temp_ss_id = self.r.create_temp_slide_show(slide_show.get_image_ids())
        return self.r.intersect_slide_shows(temp_ss_id, RedisKey.unused_images_container(self.dataset_letter))
