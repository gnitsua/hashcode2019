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


class RedisKey:
    @staticmethod
    def score_container(dataset_letter):
        return 'score-{}'.format(dataset_letter)
