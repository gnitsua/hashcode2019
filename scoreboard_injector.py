from Dataset import Dataset
from constants import DatasetLetter
from solvers.SlideShowInjectorSolver import SlideShowInjectorSolver

if __name__ == "__main__":

    for dataset_letter in DatasetLetter.__iter__():
        # dataset = Dataset(dataset_letter,start_fresh=True)
        dataset = Dataset(dataset_letter, start_fresh=False)

        solver = SlideShowInjectorSolver(dataset)
        ss = solver.solve()
