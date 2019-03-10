from DatasetLetter import DatasetLetter
from SimpleDataset import SimpleDataset
from errors import ImageInSlideShowError
from slideshow import SlideShow

if __name__ == "__main__":
    dataset_letter = DatasetLetter.A
    solution_file = "results/result-a-6.txt"
    dataset = SimpleDataset(dataset_letter.name.lower())  # load in the dataset from file

    with open(solution_file, "r") as file:
        try:
            slide_show = SlideShow.fromString(file.read(), dataset)
        except ImageInSlideShowError as e:
            print("Invalid slideshow {}".format(e.message))

        print("Score: {}".format(slide_show.get_score()))
