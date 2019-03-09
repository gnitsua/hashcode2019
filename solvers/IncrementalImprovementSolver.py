import random

from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import routing_enums_pb2

from constants import MAX_NUMBER_OF_TAGS
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
            return 100-(slide_array[from_node]-slide_array[to_node])

        return dist_callback

    def optimize(self, slide_array):
        tsp_size = len(slide_array)
        num_routes = 1
        depot = 0

        # initial_routes = [list(range(1,len(slide_array)))]#start out with the existing route(not including origin
        routing = pywrapcp.RoutingModel(tsp_size, num_routes, depot)
        # initial_assignment = routing.ReadAssignmentFromRoutes(initial_routes, True)
        search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
        # search_parameters.time_limit_ms = 10000
        # search_parameters.optimization_step = 1000
        # search_parameters.first_solution_strategy = (
        #     routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
        # search_parameters.local_search_metaheuristic = (
        #     routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
        distance_callback = self.CreateDistanceCallback(slide_array)
        routing.SetArcCostEvaluatorOfAllVehicles(distance_callback)
        # Solve the problem.
        # assignment = routing.SolveFromAssignmentWithParameters(initial_assignment, search_parameters)
        assignment = routing.SolveWithParameters(search_parameters)
        if assignment:
            result = []
            # Inspect solution.
            # Only one route here; otherwise iterate from 0 to routing.vehicles() - 1.
            route_number = 0
            node = routing.Start(route_number)
            start_node = node
            route = ''
            # result.append(slide_array[start_node])
            while not routing.IsEnd(node):
                route += str(node) + ' -> '
                node = assignment.Value(routing.NextVar(node))
                # print(node)
                result.append(slide_array[node - 1])
            print "Route:\n\n" + route
            if (len(result) != len(slide_array)):
                raise AttributeError("Solution didn't use all of the nodes ({} < {})".format(len(result), len(slide_array)))
            return result
        else:
            raise AttributeError("No solution found")

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
