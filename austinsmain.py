import time

from Dataset import Dataset
from constants import DatasetLetter
from solvers.CombiningSolver import CombiningSolver

# import matplotlib.pyplot as plt

if __name__ == "__main__":

    while (True):
        scores = []
        for dataset_letter in DatasetLetter.D:

            # dataset = Dataset(dataset_letter,start_fresh=True)
            dataset = Dataset(dataset_letter, start_fresh=False)

            solver = CombiningSolver(dataset)
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
        time.sleep(15)

    # with open(dataset_letter+"_distances.txt","w") as file:
    #
    #     distance = {}
    #     for i, image1 in enumerate(dataset):
    #         for j, image2 in enumerate(dataset):
    #             temp_slideshow = SlideShow([image1, image2])
    #             file.write("("+str(i)+","+ str(j)+"):"+str(temp_slideshow.score())+"\n")
    #             # distance["("+str(i), str(j)+")"] = temp_slideshow.score()
    #             # datasets[i][j] = (image1.tags,image2.tags)

    # np.save("distance" + dataset_letter + ".npy", distance)
    # print(distance)
    # plt.matshow(distance)
    # plt.show()

    # print(dataset)
    # solver = Solver(dataset)
    # print(solver.solve())
