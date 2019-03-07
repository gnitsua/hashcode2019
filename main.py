from Dataset import Dataset
from constants import DatasetLetter
from solvers import Solver1

if __name__ == "__main__":


    while(True):
        scores = []
        for dataset_letter in DatasetLetter.D:
            # dataset = Dataset(dataset_letter,start_fresh=True)
            dataset = Dataset(dataset_letter, start_fresh=False)

            solver = Solver1(dataset)
            while (True):
                try:
                    ss = solver.solve()
                    break
                except AttributeError as e:
                    print("redis rejected solution {}".format(e.message))

            ss.save_to_file()
            scores.append(ss.get_score())

        total = 0
        for score in scores:
            print("Score:" + str(score))
            total += score
        print(total)
