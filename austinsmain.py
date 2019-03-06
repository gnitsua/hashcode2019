from Dataset import Dataset
from solvers.SlideShowInjectorSolver import SlideShowInjectorSolver

# import matplotlib.pyplot as plt

if __name__ == "__main__":
    scores = []

    for dataset_letter in ["d"]:

        # dataset = Dataset(dataset_letter,start_fresh=True)
        dataset = Dataset(dataset_letter, start_fresh=True)

        solver = SlideShowInjectorSolver(dataset)
        ss = solver.solve()
        if (ss != None):
            scores.append(ss.get_score())
            with open("results/result-" + dataset_letter + "-" + str(ss.get_score()) + ".txt", "w") as file:
                file.write(str(ss))

    total = 0
    for score in scores:
        print("Score:" + str(score))
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
