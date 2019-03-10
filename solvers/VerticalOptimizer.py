import numpy as np
from ortools.graph import pywrapgraph

from Slide import Slide
from solvers.IncrementalImprovementSolver import IncrementalImprovementSolver


class VerticalOptimizer(IncrementalImprovementSolver):
    CHUNK_SIZE = 10000
    def optimize(self, slide_array):

        # strip all vertical slides of
        workers = []
        tasks = []

        before = 0
        for i in range(0, len(slide_array)):
            if (slide_array[i].image2 != None):  # is a vertical slide
                workers.append(slide_array[i].image2)
                tasks.append(slide_array[i].image1)
                before += len(slide_array[i].image1 + slide_array[i].image2)
                slide_array[i] = None #null this out so we know to put something here later

        if(len(workers) == 0):
            raise AttributeError("No solution found (No verticals to improve)")

        assert (len(workers) == len(tasks))
        assignment = pywrapgraph.LinearSumAssignment()
        for i in range(len(workers)):
            for j in range(len(tasks)):
                num_common_tags = len(workers[i] + tasks[j])
                assignment.AddArcWithCost( i, j , num_common_tags)

        solve_status = assignment.Solve()
        if solve_status == assignment.OPTIMAL:
            print('Total cost = ', assignment.OptimalCost())
            print()
            new_vertical_slides = [] #list of newly optimized slides
            for i in range(0, assignment.NumNodes()):
                # print('Worker %d assigned to task %d.  Cost = %d' % (
                #     i,
                #     assignment.RightMate(i),
                #     assignment.AssignmentCost(i)))
                new_vertical_slides.append(Slide(tasks[assignment.RightMate(i)],workers[i]))
            for i in range(0,len(slide_array)):
                if(slide_array[i] is None):#everywhere we took one out we should put one back
                    slide_array[i] = new_vertical_slides.pop(0)

            after = 0
            for i in range(0, len(slide_array)):
                if (slide_array[i].image2 != None):  # is a vertical slide
                    after += len(slide_array[i].image1 + slide_array[i].image2)

            print("Average number of shared tags before: {} and after {}".format(before/len(workers),after/len(workers)))


            return slide_array

        elif solve_status == assignment.INFEASIBLE:
            raise AttributeError("No solution found (No assignment is possible.)")
        elif solve_status == assignment.POSSIBLE_OVERFLOW:
            raise AttributeError("No solution found (Some input costs are too large and may cause an integer overflow.)")

        # code for interleaving horz and vertical
        # verticals = []
        # horizontals = []
        # for i in range(0, len(slide_array)):
        #     if (slide_array[i].image2 != None):
        #         verticals.append(slide_array[i])
        #     else:
        #         horizontals.append(slide_array[i])
        # result = []
        # a1 = len(verticals)
        # a2 = len(horizontals)
        #
        # for i in range(max(a1, a2)):
        #     if i < a1:
        #         result.append(verticals[i])
        #     if i < a2:
        #         result.append(horizontals[i])
        #
        # return result