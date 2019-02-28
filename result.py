from constants import FilePath

class Result():
    def __init__(self):
        pass

    def write_to_file(self, relative_path, string):
        absolute_path = FilePath.pwd + FilePath.results + relative_path
        file = open(absolute_path, 'wr')

        file.write(string)

        file.close()
