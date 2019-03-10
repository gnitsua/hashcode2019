from ImageInSlideshowError import ImageInSlideshowError
from slideshow import SlideShow
from solvers.IncrementalImprovementSolver import IncrementalImprovementSolver


class CombiningSolver(IncrementalImprovementSolver):

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

        return ss
