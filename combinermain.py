import time

from Dataset import Dataset
from RedisDataset import RedisDataset
from constants import DatasetLetter, REDIS_HOST, REDIS_PASWORD
from solvers.CombiningSolver import CombiningSolver

# import matplotlib.pyplot as plt

if __name__ == "__main__":

    while (True):
        scores = []
        for dataset_letter in [DatasetLetter.B]:

            # dataset = Dataset(dataset_letter,start_fresh=True)
            dataset = RedisDataset(dataset_letter.name.lower(), REDIS_HOST, REDIS_PASWORD, start_fresh=False)

            solver = CombiningSolver(dataset)
            while (True):
                try:
                    ss = solver.solve()
                    dataset.upload(ss)
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
        time.sleep(15)