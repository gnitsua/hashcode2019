from Parser import Parser
from result import Result

from solvers import Solver4 as Solver
solver_name = 'solver4'

input_keys = ['a', 'b', 'c', 'd', 'e']
# input_keys = ['e']

for input_key in input_keys:
    images = Parser.parse(input_key)

    print 'Solving...'
    solver = Solver(images)
    slide_show = solver.solve()

    print 'Writing result to file'
    result = Result()
    relative_path = '{}/{}_result.txt'.format(solver_name, input_key)
    string = str(slide_show)
    result.write_to_file(relative_path, string)
