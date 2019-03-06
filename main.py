from Dataset import Dataset
from solvers import Solver1

if __name__ == "__main__":
    scores = []

    for dataset_letter in ["a", "b", "c", "d", "e"]:
        with open("results/result_" + dataset_letter + ".txt", "w") as file:
            # dataset = Dataset(dataset_letter,start_fresh=True)
            dataset = Dataset(dataset_letter, start_fresh=True)

            solver = Solver1(dataset)
            while (True):
                try:
                    ss = solver.solve()
                    break
                except AttributeError as e:
                    print("redis rejected solution {}".format(e.message))

            # print(ss)
            file.write(str(ss))
            scores.append(ss.get_score())

    total = 0
    for score in scores:
        print("Score:" + str(score))
        total += score
    print(total)
