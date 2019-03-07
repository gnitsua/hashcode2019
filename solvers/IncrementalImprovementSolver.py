import random

from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

from constants import RedisKey
from slideshow import SlideShow
from solvers.BaseSolver import Solver


class IncrementalImprovementSolver(Solver):
    CHUNK_SIZE = 150

    def get_solution_to_work_on(self):
        ss_ids = self.dataset.r.zrange(RedisKey.score_container(self.dataset.dataset_letter), 0, 5, withscores=True,
                                       desc=True)
        ss_id = random.choice(ss_ids)
        assert (ss_id != None)
        slide_show_string = self.dataset.r.get(RedisKey.slide_container(self.dataset.dataset_letter, ss_id[0][5:]))
        assert (slide_show_string != None)
        ss = SlideShow.fromString(slide_show_string, self.dataset)
        assert (ss != None)
        return ss

    @staticmethod
    def distance_callback(from_node, to_node):
        return (100 - from_node - to_node)

    def optimize(self, slide_array):
        tsp_size = len(slide_array)
        num_routes = 1
        depot = 0

        routing = pywrapcp.RoutingModel(tsp_size, num_routes, depot)
        search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
        search_parameters.time_limit_ms = 120000
        search_parameters.local_search_metaheuristic = (
            routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
        routing.SetArcCostEvaluatorOfAllVehicles(self.distance_callback)
        # Solve the problem.
        assignment = routing.SolveWithParameters(search_parameters)

        if assignment:
            result = []
            # Inspect solution.
            # Only one route here; otherwise iterate from 0 to routing.vehicles() - 1.
            route_number = 0
            node = routing.Start(route_number)
            while not routing.IsEnd(node):
                node = assignment.Value(routing.NextVar(node))
            if (len(result) != len(slide_array)):
                return slide_array
            return result
        else:
            print 'No solution found.'
            return slide_array

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

        self.validate(result)
        return result

        # self.dataset.r
