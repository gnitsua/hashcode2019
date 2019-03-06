import time

import redis

from constants import DatasetLetter, RedisKey, REDIS_HOST, REDIS_PASWORD


class RedisScoreboardMoniter():
    def __init__(self,clear=False):
        self.r = redis.Redis(host=REDIS_HOST, password=REDIS_PASWORD)
        if(clear == True):
            self.r.flushall()

    def run(self):
        while (True):
            for dataset_letter in DatasetLetter.__iter__():
                print("Scores for {}".format(RedisKey.score_container(dataset_letter)))
                top_five = self.r.zrange(RedisKey.score_container(dataset_letter), 0, 5, withscores=True, desc=True)
                if (len(top_five) > 0):
                    for rank, score in enumerate(top_five):
                        print(str(rank + 1) + ". " + score[0] + "(" + str(score[1]) + ")")
                    # self.write_top_scores_to_file(dataset_letter, top_five[0][0], top_five[0][1])
                else:
                    print("no scores yet")

            time.sleep(15)

    def write_top_scores_to_file(self, dataset_letter, slideshow_id, score):
        with open("results/result_" + dataset_letter + "-" + str(int(score)) + ".txt", "w") as file:
            print(RedisKey.slide_container(dataset_letter, slideshow_id.strip(RedisKey.slideshow(dataset_letter, ""))))
            ss = self.r.get(RedisKey.slide_container(dataset_letter, slideshow_id))
            assert (ss != None)
            file.write(str(ss))


if __name__ == "__main__":
    scoreboard_moniter = RedisScoreboardMoniter()
    scoreboard_moniter.run()
