import json
import os

from enum import Enum

MAX_NUMBER_OF_TAGS = 100


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


class DatasetLetter(Enum):
    A = "a"
    B = "b"
    C = "c"
    D = "d"
    E = "e"


with open('config.json', 'r') as f:
    config = json.load(f)

REDIS_HOST = config["REDIS_HOST"]
REDIS_PASWORD = config["REDIS_PASS"]


class RedisKey:
    @staticmethod
    def score_container(dataset_letter):
        return '{}-score'.format(dataset_letter)

    @staticmethod
    def slide_container(dataset_letter, slide_show_id):
        return '{}-slides-{}'.format(dataset_letter, slide_show_id)

    @staticmethod
    def slide_show(dataset_letter, id):
        return '{}-ss-{}'.format(dataset_letter, id)

    @staticmethod
    def unused_images_container(dataset_letter):
        return dataset_letter

    @staticmethod
    def temp_slide_show(id):
        return 'temp-ss{}'.format(id)

    @staticmethod
    def unused_images_sentinal(dataset_letter):  # Needed because redis deletes empty sets
        return "{}-sentinal".format(dataset_letter)

    @staticmethod
    def dataset_lock(dataset_letter):
        return "{}-lock".format(dataset_letter)
