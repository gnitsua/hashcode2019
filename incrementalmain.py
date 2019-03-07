from Dataset import Dataset
from solvers.IncrementalImprovementSolver import IncrementalImprovementSolver
from solvers.SlideShowInjectorSolver import SlideShowInjectorSolver
from constants import DatasetLetter
# import matplotlib.pyplot as plt

if __name__ == "__main__":
    scores = []

    while(True):
        for dataset_letter in DatasetLetter.D:

            # dataset = Dataset(dataset_letter,start_fresh=True)
            dataset = Dataset(dataset_letter, start_fresh=False)

            solver = IncrementalImprovementSolver(dataset)
            while (True):
                try:
                    ss = solver.solve()
                    break
                except AttributeError as e:
                    print("redis rejected solution {}".format(e.message))

            if (ss != None):
                scores.append(ss.get_score())
                ss.save_to_file()

        total = 0
        for score in scores:
            print("Score:" + str(score))
            total += score
        print(total)
