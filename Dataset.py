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
        assert (regex.match("^.-ss", id))
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
        if (random.random() > safeness or self.r.scard(RedisKey.unused_images_container(self.dataset_letter)) == 0):
            random_image_number = random.randint(0, len(self.images) - 1)  # for unsafe gets, don't consult redis
            # while(True):
            #     key = self.r.randomkey()
            #     if(regex.match("^"+RedisKey.slideshow(self.dataset_letter,""),key)):
            #         set_to_pull_from = key
            #         break


        else:
            random_image_number = self.r.srandmember(
                RedisKey.unused_images_container(self.dataset_letter))  # only pull from unused images

        assert (random_image_number != None)
        return self.images[int(random_image_number)]

    # @cached(cache=LRUCache(maxsize=1000))
    def find_image(self, image):  # TODO: add memoization
        if (self.r.sismember(RedisKey.unused_images_container(self.dataset_letter),
                             image.id)):  # see if it's in the unused images first
            return RedisKey.unused_images_container(self.dataset_letter)
        else:
            for set in self.r.zrange(RedisKey.score_container(self.dataset_letter), 0,-1):
                if (self.r.sismember(set, image.id)):
                    return set
        raise AssertionError("never found image (" + image.id + ")")

    def find_intersections(self,slide_show):
        start = time.time()
        temp_slideshow = RedisKey.temp_slideshow(slide_show.id)
        pipeline = self.r.pipeline()
        pipeline.sadd(temp_slideshow,*slide_show.get_image_ids())
        pipeline.expire(temp_slideshow,60)#only allow temp slideshows to live for 60 seconds
        pipeline.execute()
        intersections = []
        for set in self.r.zrange(RedisKey.score_container(self.dataset_letter), 0, -1):
            assert(time.time()-start < 60)
            if(len(self.r.sinter(temp_slideshow,set))>0):
                intersections.append(set)

        return intersections


    def get_slideshow_score(self, slide_show):
        return self.r.zscore(RedisKey.score_container(self.dataset_letter), slide_show)

    def create_slideshow(self, slide_show):
        pipe = self.r.pipeline()
        pipe.set(RedisKey.slide_container(self.dataset_letter, slide_show.id),
                 slide_show.__str__())  # create the slide container
        pipe.zadd(RedisKey.score_container(self.dataset_letter), {
            RedisKey.slideshow(self.dataset_letter, slide_show.id): slide_show.get_score()})  # add entry to scoreboard
        pipe.sadd(RedisKey.slideshow(self.dataset_letter, slide_show.id), *slide_show.get_image_ids())  # add images to new slideshow
        pipe.sdiffstore(RedisKey.unused_images_container(self.dataset_letter),  # and remove them from the ununsed store
                        RedisKey.unused_images_container(self.dataset_letter),
                        RedisKey.slideshow(self.dataset_letter, slide_show.id))
        pipe.execute()
