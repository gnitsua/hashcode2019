import random

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
        if (start_fresh == True):
            self.flush_associated_keys()
        if (self.r.exists(self.dataset_letter) == 0):  # dataset doesn't currently exist in redis
            print("dataset not in redis")
            self.r.sadd(dataset_letter, *map(lambda image: image.__hash__(), self.images))
            self.r.bgsave()
        else:
            print("dataset already in redis")

    def flush_associated_keys(self):
        for key in self.r.scan_iter(match=self.dataset_letter + "*"):
            self.r.delete(key)

    def remove_slide_show(self, id):
        assert (regex.match("^.ss", id))
        pipe = self.r.pipeline()
        pipe.zrem(RedisKey.score_container(self.dataset_letter),
                  RedisKey.slideshow(self.dataset_letter, id))  # remove the entry from the score board
        pipe.delete(RedisKey.slide_container(self.dataset_letter, RedisKey.slideshow(self.dataset_letter,
                                                                                     id)))  # remove entry for the slide container
        pipe.sunionstore(RedisKey.unused_images_container(self.dataset_letter),
                         RedisKey.unused_images_container(self.dataset_letter),
                         RedisKey.slideshow(self.dataset_letter, id))
        pipe.delete(RedisKey.slideshow(self.dataset_letter, id))
        pipe.execute()

    def get(self, safeness=1):
        """
        Get a random member of the dataset
        :return: random Image() from dataset
        """
        if (random.random() > safeness):
            random_image_number = random.randint(0, len(self.images) - 1)  # for unsafe gets, don't consult redis
            # while(True):
            #     key = self.r.randomkey()
            #     if(regex.match("^"+RedisKey.slideshow(self.dataset_letter,""),key)):
            #         set_to_pull_from = key
            #         break


        else:
            set_to_pull_from = RedisKey.unused_images_container(self.dataset_letter)
            random_image_number = self.r.srandmember(set_to_pull_from)  # only pull from unused images

        assert (random_image_number != None)
        return self.images[int(random_image_number)]

    def find_image(self, image):  # TODO: add memoization
        if (self.r.sismember(RedisKey.unused_images_container(self.dataset_letter),
                             image.id)):  # see if it's in the unused images first
            return RedisKey.unused_images_container(self.dataset_letter)
        else:
            for set in self.r.scan_iter(
                    match=self.dataset_letter + "*"):  # TODO: can we just iterate through the scoreboard?
                if (self.r.type(set) == "set"):
                    if (self.r.sismember(set, image.id)):
                        return set
        raise AssertionError("never found image (" + image.id + ")")

    def get_slideshow_score(self, slide_show):
        return self.r.zscore(RedisKey.score_container(self.dataset_letter), slide_show)

    def create_slideshow(self, slide_show):
        previous_card = self.r.scard(RedisKey.unused_images_container(self.dataset_letter))
        pipe = self.r.pipeline()
        pipe.set(RedisKey.slide_container(self.dataset_letter, slide_show.id),
                 slide_show.__str__())  # create the slide container
        pipe.zadd(RedisKey.score_container(self.dataset_letter), {
            RedisKey.slideshow(self.dataset_letter, slide_show.id): slide_show.get_score()})  # add entry to scoreboard
        images = slide_show.get_images()
        image_hashes = map(lambda image: image.__hash__(), images)
        pipe.sadd(RedisKey.slideshow(self.dataset_letter, slide_show.id), *image_hashes)# add images to new slideshow
        pipe.sdiffstore(RedisKey.unused_images_container(self.dataset_letter),# and remove them from the ununsed store
                        RedisKey.unused_images_container(self.dataset_letter),
                        RedisKey.slideshow(self.dataset_letter, slide_show.id))
        pipe.execute()
        assert(previous_card-self.r.scard(RedisKey.unused_images_container(self.dataset_letter))==self.r.scard(RedisKey.slideshow(self.dataset_letter, slide_show.id)))
