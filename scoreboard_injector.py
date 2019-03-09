from Dataset import Dataset
from RedisDataset import RedisDataset
from constants import DatasetLetter, REDIS_HOST, REDIS_PASWORD
from solvers.SlideShowInjectorSolver import SlideShowInjectorSolver

if __name__ == "__main__":

    for dataset_letter in DatasetLetter:
        dataset = RedisDataset(dataset_letter.name.lower(), REDIS_HOST, REDIS_PASWORD, start_fresh=False)

        solver = SlideShowInjectorSolver(dataset)
        ss = solver.solve()
