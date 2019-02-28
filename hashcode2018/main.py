from hashcode2018.InputFile import InputFile
from hashcode2018.Solver import Solver

if __name__ == "__main__":
    input = InputFile("input_files/a_example.in")
    solver = Solver(input)
    solution = solver.solve()
    print(solution)
    solution.show()
