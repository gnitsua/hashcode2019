from Parser import Parser
from result import Result

from solvers import Solver5 as Solver
solver_name = 'solver5'

# input_keys = ['a', 'b', 'c', 'd', 'e']
input_keys = ['d']

for input_key in input_keys:
    lines = Parser.get_lines(input_key)

    print 'Solving...'
    solver = Solver(lines)
    slide_show = solver.solve(input_key)

    print 'Writing result to file'
    result = Result()
    relative_path = '{}/{}_result.txt'.format(solver_name, input_key)
    string = str(slide_show)
    result.write_to_file(relative_path, string)
