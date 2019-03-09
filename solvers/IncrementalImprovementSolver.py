import random

from slideshow import SlideShow
from solvers.BaseSolver import Solver


class IncrementalImprovementSolver(Solver):
    CHUNK_SIZE = 2000

    def get_solution_to_work_on(self):
        slide_shows = self.dataset.slide_shows()
        assert (len(slide_shows) > 0)
        slide_show_id = random.choice(slide_shows)
        return self.dataset.get_slide_show(slide_show_id)

    @staticmethod
    def CreateDistanceCallback(slide_array):
        def dist_callback(from_node, to_node):
            return 100 - (slide_array[from_node] - slide_array[to_node])

        return dist_callback

    def optimize(self, slide_array):
        raise NotImplementedError("IncrementalImprovementSolver is abstract")

    def solve(self):

        # get the old sideshow
        old_ss = self.get_solution_to_work_on()
        old_ss_slides = old_ss.slides
        if (len(old_ss_slides) > self.CHUNK_SIZE):
            # break off a chunk
            start = random.randint(0, len(old_ss_slides) - self.CHUNK_SIZE - 1)
            end = start + self.CHUNK_SIZE
            chunk_to_improve = old_ss_slides[start:end]
        else:
            start = 0
            end = len(old_ss_slides)
            chunk_to_improve = old_ss_slides

        optimized_chunk = self.optimize(chunk_to_improve)

        new_slide_list = old_ss_slides[0:start] + optimized_chunk + old_ss_slides[end:]

        result = SlideShow(self.dataset.dataset_letter)
        for i, slide in enumerate(new_slide_list):
            result.add_slide(slide)

        return result

        # self.dataset.r
