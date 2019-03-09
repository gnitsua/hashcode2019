from RedisDataset import RedisDataset
from constants import DatasetLetter
from constants import REDIS_HOST
from constants import REDIS_PASWORD
from solvers import Solver1

if __name__ == "__main__":

    scores = []
    for dataset_letter in [DatasetLetter.A]:
        dataset = RedisDataset(dataset_letter.name.lower(), REDIS_HOST, REDIS_PASWORD, start_fresh=False)

        solver = Solver1(dataset)
        try:
                ss = solver.solve()
        print("Solution found, uploading")
        dataset.upload(ss)
        scores.append(ss.get_score())
        ss.save_to_file()
        except Exception as e:
            print("Failed to find a solution to {} ({})".format(dataset_letter, e.message))

    total = 0
    for score in scores:
        print("Score:" + str(score))
        total += score
    print(total)
