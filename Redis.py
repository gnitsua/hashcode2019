import uuid

import redis

from constants import RedisKey
from errors import ImageInAnotherSlideShowError


class Redis():
    def __init__(self, host, password):
        self.r = redis.Redis(host=host, password=password)

    def does_exist(self, dataset_letter):
        return self.r.exists(RedisKey.unused_images_sentinal(dataset_letter)) > 0

    def add_dataset(self, dataset):
        if (not self.does_exist(dataset.dataset_letter)):
            pipe = self.r.pipeline()
            pipe.sadd(RedisKey.unused_images_container(dataset.dataset_letter),
                      *map(lambda image: image.__hash__(), dataset.images))
            pipe.set(RedisKey.unused_images_sentinal(dataset.dataset_letter), "True")
            pipe.execute()
            self.save()  # since this is a big change, make sure it's saved

    def remove_dataset(self, dataset_letter):
        pass

    def get_unused_images(self, dataset_letter):
        return self.r.smembers(RedisKey.unused_images_container(dataset_letter))

    def get_num_unused_images(self, dataset_letter):
        return self.r.scard(RedisKey.unused_images_container(dataset_letter))

    def get_random_unused_image(self, dataset_letter):
        """
        returns a random image from the dataset's un-used images
        :param dataset_letter:
        :return: Image or None
        """
        return self.r.srandmember(RedisKey.unused_images_container(dataset_letter))  # only pull from unused images

    def get_scoreboard(self, dataset_letter, start=0, end=-1):
        raw_result = self.r.zrange(RedisKey.score_container(dataset_letter), start, end, withscores=True, desc=True)
        return map(lambda result: (result[0][5:], result[1]), raw_result)  # strip of the dataset letter

    def get_score(self, dataset_letter, slide_show_id):
        return self.r.zscore(RedisKey.score_container(dataset_letter),
                             RedisKey.slide_show(dataset_letter, slide_show_id))

    def get_slide_show_image_ids(self, slide_show_id, dataset_letter):
        return self.r.smembers(RedisKey.slide_show(dataset_letter, slide_show_id))

    def get_slide_show_string(self, slide_show_id, dataset_letter):
        return self.r.get(RedisKey.slide_container(dataset_letter, slide_show_id))

    def get_all_slide_shows(self, dataset_letter):
        result = []
        for key in self.r.scan_iter(match=dataset_letter + "-ss-*"):
            result.append(key[5:])  # TODO: way to convert back to actual slideshow id (remove dataset letter)
        return result

    def create_slide_show(self, slide_show_id, image_id_array, score, slides_string, dataset_letter):
        """
        creates a slideshow by moving all images to the slide show from the unused container
        :param slideshow_id:
        :param image_id_array:
        :param score:
        :param slides_string:
        :param dataset_letter:
        :raises AssertionError: if something went wrong with the move
        """
        slide_show_key = RedisKey.slide_show(dataset_letter, slide_show_id)
        scoreboard_key = RedisKey.score_container(dataset_letter)
        unused_images_key = RedisKey.unused_images_container(dataset_letter)
        # make sure the slideshow doesn't already exist
        assert (self.r.zscore(scoreboard_key, slide_show_key) is None)
        assert (self.r.get(RedisKey.slide_container(dataset_letter, slide_show_id)) is None)
        assert (self.r.scard(slide_show_key) == 0)

        # make sure all the slides are in the unused container
        temp_slide_show_id = self.create_temp_slide_show(image_id_array)
        try:
            assert (len(self.intersect_slide_shows(temp_slide_show_id, unused_images_key)) == len(image_id_array))
        except AssertionError:
            raise ImageInAnotherSlideShowError("Some images not in unused image set")

        # move the images from the unused container
        pipe = self.r.pipeline()
        for image_id in image_id_array:
            pipe.smove(unused_images_key, slide_show_key, image_id)

        # create scoreboard entry
        pipe.zadd(scoreboard_key, {slide_show_key: score})
        # creat slides container
        pipe.set(RedisKey.slide_container(dataset_letter, slide_show_id), slides_string)
        pipe.execute()

    def create_temp_slide_show(self, image_id_array):
        """
        Creates a temp slide show.
        Notes:
        1. temp slide shows are not associated with a dataset_letter and will
        expire after 60 seconds
        2. the temp slideshow is not garunteed to be valid, it may contain images that are used in another slide show
        3. the temp slideshow does not have a slides container or scoreboard entry
        :param image_id_array: Array of image ids to add
        :return: id of temp slide show
        """
        id = "temp-{}".format(uuid.uuid4())
        pipeline = self.r.pipeline()
        pipeline.sadd(id, *image_id_array)
        pipeline.expire(id, 60)  # only allow temp slideshows to live for 60 seconds
        pipeline.execute()
        return id

    def remove_slide_show(self, slide_show_id, dataset_letter):
        """
        Removes slideshow by moving all images back to the unused container. Redis deletes empty sets
        Raises as
        :param slideshow_id:
        :param dataset_letter:
        :raises AssertionError: if something went wrong with the move
        """
        slide_show_key = RedisKey.slide_show(dataset_letter, slide_show_id)
        pipe = self.r.pipeline()
        for image_id in self.r.smembers(slide_show_key):
            pipe.smove(slide_show_key, RedisKey.unused_images_container(dataset_letter), image_id)
        pipe.execute()

    def intersect_slide_shows(self, slide_show_id_1, slide_show_id_2):
        return self.r.sinter(slide_show_id_1, slide_show_id_2)

    def find_connected_components(self, slide_show_key, dataset_letter):
        """
        Finds all of the slideshow ids that share slides with a give slideshow
        Warning: if using a temp slideshow, you must make sure that the slideshow does not expire before this method exits
        :param slide_show_id: id of a slideshow to intersect
        :param dataset_letter:
        """
        result = []
        for set in self.r.scan_iter(match=RedisKey.slide_show(dataset_letter, "") + "*"):
            if (len(self.intersect_slide_shows(slide_show_key, set)) > 0):
                result.append(set[5:])  # TODO: converting key back to id
        return result

    def flush_associated_keys(self, dataset_letter):
        pipe = self.r.pipeline()
        for key in self.r.scan_iter(match=dataset_letter + "*"):
            pipe.delete(key)
        pipe.execute()

    def save(self):
        self.r.bgsave()
