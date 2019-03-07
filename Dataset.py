import random
import time

import redis
import regex as regex

from Parser import Parser
from constants import REDIS_HOST, REDIS_PASWORD, RedisKey

random.seed()


class Dataset():
    def __init__(self, dataset_letter, start_fresh=False):
        self.dataset_letter = dataset_letter
        self.images = Parser.parse(dataset_letter)
        self.r = redis.Redis(host=REDIS_HOST, password=REDIS_PASWORD)
        if (start_fresh == True or self.r.exists(RedisKey.unused_images_sentinal(self.dataset_letter)) == 0):
            print("dataset not in redis")
            self.flush_associated_keys()
            pipe = self.r.pipeline()
            pipe.sadd(RedisKey.unused_images_container(self.dataset_letter),
                      *map(lambda image: image.__hash__(), self.images))
            pipe.set(RedisKey.unused_images_sentinal(self.dataset_letter), "True")
            pipe.execute()
            self.r.bgsave()
        else:
            print("dataset already in redis")

    def flush_associated_keys(self):
        for key in self.r.scan_iter(match=self.dataset_letter + "*"):
            self.r.delete(key)

    def remove_slide_show(self, id):
        assert (regex.match("^.-ss", id))
        # assert (self.r.scard(id) > 0)
        # starting_number_of_unused = self.r.scard(RedisKey.unused_images_container(self.dataset_letter))
        # number_in_slideshow = self.r.scard(id)
        pipe = self.r.pipeline()
        pipe.zrem(RedisKey.score_container(self.dataset_letter), id)  # remove the entry from the score board
        pipe.delete(RedisKey.slide_container(self.dataset_letter, id))  # remove entry for the slide container
        pipe.sunionstore(RedisKey.unused_images_container(self.dataset_letter),
                         RedisKey.unused_images_container(self.dataset_letter), id)
        pipe.delete(id)
        pipe.execute()
        # ending_number_of_unused = self.r.scard(RedisKey.unused_images_container(self.dataset_letter))
        # assert (ending_number_of_unused - starting_number_of_unused == number_in_slideshow)

    def get(self, safeness=1):
        """
        Get a random member of the dataset
        :return: random Image() from dataset
        """
        if (random.random() > safeness or self.r.scard(RedisKey.unused_images_container(self.dataset_letter)) == 0):
            random_image_number = random.randint(0, len(self.images) - 1)  # for unsafe gets, don't consult redis
        else:
            random_image_number = self.r.srandmember(
                RedisKey.unused_images_container(self.dataset_letter))  # only pull from unused images

        assert (random_image_number != None)
        return self.images[int(random_image_number)]

    def find_intersections(self, slide_show):
        start = time.time()
        temp_slideshow = RedisKey.temp_slideshow(slide_show.id)
        pipeline = self.r.pipeline()
        pipeline.sadd(temp_slideshow, *slide_show.get_image_ids())
        pipeline.expire(temp_slideshow, 60)  # only allow temp slideshows to live for 60 seconds
        pipeline.execute()
        intersections = []
        for set in self.r.scan_iter(match=RedisKey.slideshow(self.dataset_letter, "") + "*"):
            assert (time.time() - start < 60)
            if (len(self.r.sinter(temp_slideshow, set)) > 0):
                intersections.append(set)

        return intersections

    def get_slideshow_score(self, slide_show):
        return self.r.zscore(RedisKey.score_container(self.dataset_letter), slide_show)

    def create_slideshow(self, slide_show):
        starting_number_of_unused = self.r.scard(RedisKey.unused_images_container(self.dataset_letter))
        pipe = self.r.pipeline()
        pipe.set(RedisKey.slide_container(self.dataset_letter, slide_show.id),
                 slide_show.__str__())  # create the slide container
        pipe.zadd(RedisKey.score_container(self.dataset_letter), {
            RedisKey.slideshow(self.dataset_letter, slide_show.id): slide_show.get_score()})  # add entry to scoreboard
        pipe.sadd(RedisKey.slideshow(self.dataset_letter, slide_show.id), *map(lambda image: image.__hash__(), slide_show.get_images()))  # add images to new slideshow
        pipe.sdiffstore(RedisKey.unused_images_container(self.dataset_letter),  # and remove them from the ununsed store
                        RedisKey.unused_images_container(self.dataset_letter),
                        RedisKey.slideshow(self.dataset_letter, slide_show.id))
        pipe.execute()

        ending_number_of_unused = self.r.scard(RedisKey.unused_images_container(self.dataset_letter))
        number_added_to_slideshow = self.r.scard(RedisKey.slideshow(self.dataset_letter, slide_show.id))
        assert (number_added_to_slideshow == len(slide_show.get_image_ids()))
        assert (starting_number_of_unused - ending_number_of_unused == number_added_to_slideshow)

    def print_associated_keys(self):
        for key in self.r.keys(RedisKey.unused_images_container(self.dataset_letter) + "*"):
            print(key)
