from Slide import Slide
from image import Image
from slideshow import SlideShow


class Solver():
    def __init__(self,dataset):
        self.dataset = dataset

    def solve(self):
        test1 = Image(1, "V", set({1, 2, 3}))
        test2 = Image(2, "V", set({3, 4, 53}))
        test3 = Image(3, "V", set({3, 4, 5}))
        slide = Slide(test1, test2)
        slide2 = Slide(test1, test3)

        ss = SlideShow([slide,slide2])
        return ss