from Solver import Solver
import random

class GreedySolver(Solver):
    def __init__(self, input_file):
        super().__init__(input_file)

    def solve(self):
        available_rides = self.input_file.rides
        while(len(available_rides) > 0):
            pass