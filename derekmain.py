from Parser import Parser

from solvers import Solver1 as Solver

images = Parser.parse("a")

solver = Solver(images)

# slide_show = solver.solve()

