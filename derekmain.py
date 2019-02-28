from Parser import Parser
from result import Result

from solvers import Solver1 as Solver

file = 'c'
solver_name = 'solver1'

images = Parser.parse(file)

solver = Solver(images)

slide_show = solver.solve()

result = Result()
relative_path = '{}/{}_result.txt'.format(solver_name, file)
string = str(slide_show)
result.write_to_file(relative_path, string)
