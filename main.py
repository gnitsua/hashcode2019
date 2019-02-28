from Parser import Parser
from Solver import Solver

if __name__ == "__main__":
    dataset = Parser.parse("a")
    solver = Solver(dataset)
    print(solver.solve())
