from slideshow import SlideShow
from solvers.BaseSolver import Solver
from ImageInSlideshowError import ImageInSlideshowError

class CombiningSolver(Solver):

    def solve(self):
        ss1 = self.get_solution_to_work_on()
        ss2 = self.get_solution_to_work_on()

        ss = SlideShow(self.dataset.dataset_letter)
        for slide in ss1.slides:
            try:
                ss.add_slide(slide)
            except ImageInSlideshowError as e:
                print e

        for slide in ss2.slides:
            try:
                ss.add_slide(slide)
            except ImageInSlideshowError as e:
                print e

        self.validate(ss)
        return ss