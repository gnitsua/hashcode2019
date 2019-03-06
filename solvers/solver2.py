import random
import time

from Slide import Slide
from constants import DatasetLetter
from slideshow import SlideShow
from solvers.BaseSolver import Solver


class Solver2(Solver):
    known_horizontal = {
        DatasetLetter.A: 9,
        DatasetLetter.B: 0,
        DatasetLetter.C: 1,
        DatasetLetter.D: 0,
        DatasetLetter.E: None,

    }

    def solve(self):
        random.seed()

        # starting_node = self.dataset.get(safeness=0.5)
        # while (starting_node.orientation != Orientation.horizontal):
        #     starting_node = self.dataset.get()
        starting_node = self.dataset.images[self.known_horizontal[self.dataset.dataset_letter]]  # known horizontal

        ss = SlideShow(self.dataset.dataset_letter)
        # print(starting_node)
        ss.add_slide(Slide(starting_node))

        start = time.time()
        while (time.time() - start < 60):
            self.add_slide(ss)

        self.validate(ss)
        return ss

    def add_slide(self, slideshow):
        max_score = 0
        for _ in range(5):
            try:
                random_slide = self.dataset.get(safeness=0)
                slideshow.add_slide(Slide(random_slide))
                score = slideshow.get_score()
                if (score > max_score):
                    max_score = score
                else:
                    slideshow.pop()
            except AttributeError as e:
                print("invalid slideshow (" + e.message) + ")"
