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

        ss = SlideShow()
        # print(starting_node)
        ss.add_slide(Slide(starting_node))
        # ss.add_slide(Slide(second_node))

        while(len(ss.slides) < 1000 and len(ss.slides) < len(self.dataset)*0.4):
            self.add_slide(ss)
        return ss



    def add_slide(self, slideshow):
        options = set([random.randint(0,len(self.dataset)-1) for _ in range(1)])

        max = 0
        for option in options:
            try:
                slideshow.add_slide(Slide(self.dataset[option]))
                score = slideshow.score()

                if(score > max):
                    max = score
                else:
                    slideshow.pop()
            except AttributeError as e:
                pass
                # print("invalid slideshow ("+e.message)+")"

