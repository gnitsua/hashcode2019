import random

from Slide import Slide
from constants import Orientation
from slideshow import SlideShow
from solvers.BaseSolver import Solver


class Solver2(Solver):
    def solve(self):
        random.seed()

        starting_node = self.dataset[random.randint(0, len(self.dataset)-1)]
        while(starting_node.orientation != Orientation.horizontal):
            starting_node = self.dataset[random.randint(0, len(self.dataset) - 1)]

        ss = SlideShow(self.dataset.dataset_letter)
        # print(starting_node)
        ss.add_slide(Slide(starting_node))
        # ss.add_slide(Slide(second_node))
        while(len(ss.slides) < 2):
            self.add_slide(ss)

        ss.finalize()
        return ss



    def add_slide(self, slideshow):
        options = set([random.randint(0,len(self.dataset)-1) for _ in range(5)])

        max = 0
        for option in options:
            try:
                slideshow.add_slide(Slide(self.dataset[option]))
                score = slideshow.get_score()

                if(score > max):
                    max = score
                else:
                    slideshow.pop()
            except AttributeError as e:
                pass
                # print("invalid slideshow ("+e.message)+")"

