import numpy as np

from Dataset import Dataset
from Parser import Parser
from slideshow import SlideShow
from solvers.solver2 import Solver2

# import matplotlib.pyplot as plt

if __name__ == "__main__":
    scores = []

    for dataset_letter in ["c"]:
        with open("results/result_"+dataset_letter+".txt", "w") as file:
            # dataset = Dataset(dataset_letter,start_fresh=True)
            dataset = Dataset(dataset_letter,start_fresh=False)

            solver = Solver2(dataset)
            while(True):
                # try:
                    ss = solver.solve()
                    break
                # except AttributeError as e:
                #     print("redis rejected solution {}".format(e.message))

            print(ss)
            file.write(str(ss))
            scores.append(ss.get_score())

    total = 0
    for score in scores:
        print("Score:"+str(score))
        total += score
    print(total)



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
