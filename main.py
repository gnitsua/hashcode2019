from InputFile import InputFile
from Solver import Solver

if __name__ == "__main__":
    input = InputFile("input_files/a_example.in")
    solver = Solver(input)
    solution = solver.solve()
    solution.show()
