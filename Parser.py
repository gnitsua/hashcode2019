from os import listdir

from constants import FilePath, InputFile
from image import Image


class Parser():
    @staticmethod
    def get_data_sets():
        data_dir = FilePath.pwd + FilePath.data
        all_data_sets = listdir(data_dir)

        data_set_map = {}
        for data_set in all_data_sets:
            key = data_set.split('_')[0]
            absolute_path = data_dir + data_set
            data_set_map.update({key: absolute_path})

        return data_set_map

    @staticmethod
    def parse_images(data_set):
        # Returns a list of Image objects
        images = []
        file = open(data_set, 'r')

        for line_no, line in enumerate(file):
            if line_no < InputFile.lines_to_skip:
                continue

            line = line.replace('\n', '')

            data = line.split(' ')

            id = line_no - InputFile.lines_to_skip
            orientation = data[0]
            number_of_tags = data[1]
            tags = data[2:]

            image = Image(id, orientation, tags)
            images.append(image)

        file.close()

        return images

    @staticmethod
    def parse(data_set_letter):
        # Command line args, list files to test
        # If no file names are supplied then test all
        all_data_sets = Parser.get_data_sets()

        keys_to_parse = data_set_letter or all_data_sets.keys()

        data_sets = [file for key, file in all_data_sets.iteritems() if key in keys_to_parse]

        for data_set in data_sets:
            print('Parsing', data_set)
            images = Parser.parse_images(data_set)

        return images
