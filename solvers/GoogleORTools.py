from ortools.constraint_solver import pywrapcp

from solvers.IncrementalImprovementSolver import IncrementalImprovementSolver


class GoogleORTools(IncrementalImprovementSolver):
    def __init__(self, dataset):
        IncrementalImprovementSolver.__init__(self, dataset)

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