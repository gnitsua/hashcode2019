import matplotlib.pyplot as plt

from Solution import Solution


class Solver():
    def __init__(self, input_file):
        self.input_file = input_file

    def solve(self):
        solution = Solution(self.input_file.map)
        for ride in self.input_file.rides:
            solution.addRide(ride)
        return solution