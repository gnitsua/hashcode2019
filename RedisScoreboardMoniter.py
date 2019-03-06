import time

import redis

from Dataset import Dataset
from constants import DatasetLetter, REDIS_HOST, REDIS_PASWORD


class RedisScoreboardMoniter():
    def __init__(self):
        self.r = redis.Redis(host=REDIS_HOST, password=REDIS_PASWORD)

    def run(self):
        while (True):
            for dataset_letter in DatasetLetter.__iter__():
                print("Scores for " + dataset_letter)
                top_five = self.r.zrange(Dataset.get_dataset_score_container_key(dataset_letter), 0, 5, withscores=True)
                if (len(top_five) > 0):
                    for rank, score in enumerate(top_five):
                        print(str(rank) + ". " + score[0] + "(" + str(score[1]) + ")")
                    self.write_top_scores_to_file(dataset_letter, top_five[0][0], top_five[0][1])
                else:
                    print("no scores yet")
            time.sleep(15)

    def write_top_scores_to_file(self, dataset_letter, slideshow_id, score):
        with open("results/result_" + dataset_letter + "-" + str(int(score)) + ".txt", "w") as file:
            ss = self.r.get(slideshow_id)
            print(ss)
            if (ss != None):
                file.write(str(ss))
            else:
                file.write("")


if __name__ == "__main__":
    scoreboard_moniter = RedisScoreboardMoniter()
    scoreboard_moniter.run()
