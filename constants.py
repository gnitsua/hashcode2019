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
