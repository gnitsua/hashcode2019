import time

from RedisDataset import RedisDataset
from constants import DatasetLetter
from constants import REDIS_HOST
from constants import REDIS_PASWORD
from solvers.IncrementalImprovementSolver import IncrementalImprovementSolver

if __name__ == "__main__":

    scores = []
    while(True):
        for dataset_letter in [DatasetLetter.E]:
            dataset = RedisDataset(dataset_letter.name.lower(), REDIS_HOST, REDIS_PASWORD, start_fresh=False)

            solver = IncrementalImprovementSolver(dataset)
            try:
                start = time.time()
                ss = solver.solve()
                print("Solution found in {}, uploading".format(time.time()-start))
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
