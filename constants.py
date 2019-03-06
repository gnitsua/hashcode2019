import json
import os


class Orientation:
    horizontal = 'horizontal'
    vertical = 'vertical'


class FilePath:
    data = '/data_sets/'
    results = '/results/'
    pwd = os.path.dirname(os.path.realpath(__file__))


class InputFile:
    lines_to_skip = 1


UNASSIGNED_IMAGE = "none"


class DatasetLetter:
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"

    @classmethod
    def __iter__(cls):
        return [cls.A, cls.B, cls.C, cls.D, cls.E].__iter__()


with open('config.json', 'r') as f:
    config = json.load(f)

REDIS_HOST = config["REDIS_HOST"]
REDIS_PASWORD = config["REDIS_PASS"]

class RedisKey:
    @staticmethod
    def score_container(dataset_letter):
        return '{}-score'.format(dataset_letter)

    @staticmethod
    def slide_container(dataset_letter,slideshow_id):
        return '{}-slides-{}'.format(dataset_letter,slideshow_id)

    @staticmethod
    def slideshow(dataset_letter,id):
        return '{}-ss-{}'.format(dataset_letter,id)

    @staticmethod
    def unused_images_container(dataset_letter):
        return dataset_letter

    @staticmethod
    def temp_slideshow(id):
        return 'temp-ss{}'.format(id)