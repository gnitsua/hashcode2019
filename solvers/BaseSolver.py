from Slide import Slide
from image import Image
from slideshow import SlideShow


class Solver():
    def __init__(self, dataset):
        self.dataset = dataset

    def solve(self):
        test1 = Image(1, "V", set({1, 2, 3}))
        test2 = Image(2, "V", set({3, 4, 53}))
        test3 = Image(3, "V", set({3, 4, 5}))
        slide = Slide(test1, test2)
        slide2 = Slide(test1, test3)

        ss = SlideShow([slide, slide2])
        return ss

    def validate(self, slideshow):
        score = slideshow.get_score()

        # figure out which slideshows would need to die
        slideshows_to_kill = self.dataset.find_intersections(slideshow)

        print("Slideshows to kill {}".format(slideshows_to_kill))

        # figure out if we should kill them
        for slideshow_to_kill in slideshows_to_kill:
            slide_show_score = self.dataset.get_slideshow_score(slideshow_to_kill)

            if (slide_show_score > score):
                raise AttributeError(
                    "Slide currently in use by a slideshow with a higher score ({}>{})".format(slide_show_score, score))


        print("Adding {}".format(slideshow.id))

        # so let's kill those slide shows
        for slideshow_to_kill in slideshows_to_kill:
            self.dataset.remove_slide_show(slideshow_to_kill)#TODO does this need to be atomic

        self.dataset.create_slideshow(slideshow)
