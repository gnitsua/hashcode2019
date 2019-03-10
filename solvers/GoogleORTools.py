from ortools.constraint_solver import pywrapcp, routing_enums_pb2

from solvers.IncrementalImprovementSolver import IncrementalImprovementSolver
import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

class GoogleORTools(IncrementalImprovementSolver):
    CHUNK_SIZE = 1000
    def __init__(self, dataset):
        IncrementalImprovementSolver.__init__(self, dataset)

    @staticmethod
    def CreateDistanceCallback(slide_array):
        def dist_callback(from_node, to_node):
            return 100-(slide_array[from_node] - slide_array[to_node])

        return dist_callback

    def optimize(self, slide_array):
        tsp_size = len(slide_array)
        num_routes = 1
        depot = 0

        # initial_routes = [list(range(1,len(slide_array)))]#start out with the existing route(not including origin
        routing = pywrapcp.RoutingModel(tsp_size, num_routes, depot)
        # initial_assignment = routing.ReadAssignmentFromRoutes(initial_routes, True)
        search_parameters = pywrapcp.RoutingModel.DefaultSearchParameters()
        search_parameters.time_limit_ms = 10000
        search_parameters.optimization_step = 100
        search_parameters.log_search = True
        # search_parameters.use_light_propagation = False
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