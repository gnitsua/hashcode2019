import time
import redis

from Dataset import Dataset
from constants import DatasetLetter, RedisKey


class RedisScoreboardMoniter():
    def __init__(self):
        self.r = redis.Redis(host="192.168.99.100")

    def run(self):
        while (True):
            for dataset_letter in DatasetLetter.__iter__():
                print("Scores for "+dataset_letter)
                for rank,score in enumerate(self.r.zrange(RedisKey.score_container(dataset_letter), 0, 5, withscores=True)):
                    print(str(rank)+". "+score[0]+"("+str(score[1])+")")
                    self.write_top_scores_to_file()
            time.sleep(15)

    def write_top_scores_to_file(self):
        for dataset_letter in DatasetLetter.__iter__():
            top_ss_id = self.r.zrange(RedisKey.score_container(dataset_letter), 0, 0)
            with open("results/result_"+dataset_letter+"-"+str(int(top_ss_id[0][1]))+".txt","w") as file:
                top_ss_id = self.r.zrange(RedisKey.score_container(dataset_letter), 0, 0)
                ss = self.r.get(top_ss_id[0][0])
                if(ss != None):
                    file.write(str(ss))
                else:
                    file.write("")


if __name__ == "__main__":
    scoreboard_moniter = RedisScoreboardMoniter()
    scoreboard_moniter.run()