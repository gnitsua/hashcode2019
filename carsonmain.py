import itertools
import math
import random

from Dataset import Dataset
from Slide import Slide
from constants import Orientation
from slideshow import SlideShow


def score(set1, set2):
    inter = len(set1.intersection(set2))
    disjoint1 = len(set1) - inter
    disjoint2 = len(set2) - inter
    return min(inter, disjoint1, disjoint2)


def validateScore(fn, dfn):
    data = parseFile(dfn)
    slides = parseSlideshow(fn)
    print "Number of pictures: ", len(data)
    print "Number of slides: ", len(slides)

    slideSets = []
    for slide in slides:
        if len(slide) == 1:
            set1 = data[slide[0]][2]
            slideSets.append(set1)
        else:
            set1 = data[slide[0]][2]
            set2 = data[slide[1]][2]
            combinedSet = set1.union(set2)
            slideSets.append(combinedSet)

    total = 0
    index = 0
    while index < len(slideSets) - 1:
        total += score(slideSets[index], slideSets[index + 1])
        index += 1
    return total


def parseSlideshow(filename):
    slides = []
    for file in [filename]:
        with open(file) as fh:
            numLines = next(fh)
            numLines = numLines.strip()
            for line in fh:
                stripped = line.strip()
                dataInt = map(int, stripped.split())
                slides.append(dataInt)
    if int(numLines) != len(slides):
        print "Error reading slideshow... line 1 does not equal number of slides in file..."
        return []
    else:
        return slides


def parseFile(filename):
    data = []
    for datafile in [filename]:
        pid = -1
        with open(datafile) as fh:
            next(fh)
            for line in fh:
                stripped = line.strip()
                dataline = stripped.split(" ")
                pid += 1
                kind = dataline[0]
                numtags = dataline[1]
                tags = set(dataline[2:])
                data.append([pid, kind, tags])
    return data



def generateVslides(vertical_images,num):
    if(num > len(vertical_images)):
        sample = len(vertical_images)
    else:
        sample = num
    return set(map(lambda tuple: Slide(tuple[0], tuple[1]), itertools.combinations(random.sample(vertical_images,sample), 2)))


# def generateRandomVSlides(Vs):
#     Vint = []
#     random.shuffle(Vs)
#
#     index = 0
#     while index < len(Vs) - 1:
#         i = Vs[index]
#         j = Vs[index + 1]
#         unioned = i[2].union(j[2])
#         Vint.append([set((i, j)), 'V', unioned])
#         index += 2
#     return Vint


def remove_all_slides_with_image(image, slides):
    result = set(slides)
    for slide in slides:
        if (slide.image1 == image or slide.image2 == image):
            result.remove(slide)
    return result


def solve1(Hs, vertical_images, dataset_letter):
    assert(len(vertical_images) % 2 == 0)
    # pick a random H to start with
    # force search until a score >= SCOREX is found
    # add, remove ID, reset SCOREX, and repeat
    count = 0
    solution = SlideShow(dataset_letter)
    # solution = [count]
    total = 0
    SCOREXinit = 5  # VARY ME

    random.seed()

    Vs = generateVslides(vertical_images, 500)
    if len(Hs) != 0:
        start = random.sample(Hs, 1)[0]  # VARY ME (?)
        Hs.remove(start)
    else:
        start = random.sample(Vs, 1)[0]
        vertical_images.remove(start.image1)
        vertical_images.remove(start.image2)

    solution.add_slide(start)

    while True:
        num_horizontal = len(Hs)
        if(len(vertical_images)>1):
            num_vertical = math.factorial(len(vertical_images)) / math.factorial(len(vertical_images) - 2)
        else:
            num_vertical = len(vertical_images)
        num_allSlidesPossible = num_horizontal + num_vertical
        if(num_allSlidesPossible < 1):
            break
        ATTEMPTSX = num_allSlidesPossible  # VARY ME, large effect on score and time
        SCOREX = SCOREXinit
        attempts = 0
        score_before = solution.get_score()
        Vs = generateVslides(vertical_images,500)
        while True:
            if(random.randint(0,num_allSlidesPossible) < num_horizontal or num_vertical < 1):#do a horizontal
                B = random.sample(Hs, 1)[0]  # pick a random slide
                orientation = Orientation.horizontal
            else: #do a vertical
                B = random.sample(Vs, 1)[0]  # pick a random slide
                orientation = Orientation.vertical


            # B = random.sample(allSlidesPossible, 1)[0]  # pick a random slide
            before = solution.get_score()
            solution.add_slide(B)  # add it to the slideshow
            during = solution.get_score()
            if (solution.get_score() - score_before < SCOREX):  # the increase in score is not enough to keep this slide
                if attempts < ATTEMPTSX:
                    attempts += 1
                else:
                    SCOREX = SCOREX - 1
                    attempts = 0  # COULD GO IN ORDER, WHEN CONTINUING, KEEP GOING IN A CIRCLE TO ALLOW FOR A HIGHER SCORE TO REAPPEAR
                solution.pop()  # so go back a step


            else:  # we found our next slide
                break

        if(orientation == Orientation.horizontal):
            Hs.remove(solution.slides[-1])
        else:
            last_slide = solution.slides[-1]
            vertical_images.remove(last_slide.image1)
            vertical_images.remove(last_slide.image2)

        # allSlidesPossible = remove_all_slides_with_image(B.image1, allSlidesPossible)
        # allSlidesPossible = remove_all_slides_with_image(B.image2, allSlidesPossible)
        if count % 100 == 0:
            if ATTEMPTSX != 0:
                print solution.get_score(), " / #", count, " / ", num_allSlidesPossible, " left / ", 100 * (
                            float(attempts) / num_allSlidesPossible), "% tried"

        count+=1

    return solution


if __name__ == "__main__":

    ##### READ DATA #####
    dataset_letter = "d"
    dataset = Dataset(dataset_letter)
    print "Read ", len(dataset.images), " lines from data file: ", dataset_letter

    ##### SEPARATE RAW DATA INTO Vs and Hs #####
    vertical_images = set()
    Hs = set()
    for i in dataset.images:
        if i.orientation == Orientation.vertical:
            vertical_images.add(i)
        else:
            Hs.add(Slide(i))

    # VIDs = [item.id for item in vertical_images]

    ##### GENERATE ALL POSSIBLE VERTICALS #####
    # print "Generating verticals from ", len(vertical_images), " vertical pictures"

    # print "Generating ALL..."
    # Vint = generateVslides(Vs,500)  # okay for low numbers of verticals, 500 works
    # OR VARY
    # print "Generating randoms..."
    # Vint = generateRandomVSlides(Vs)

    # print "Calculated vertical combos... (", len(Vint), ")"
    # Vint is a list of all possible vertical combos (aka slides) [{ID1, ID2}, # of tags combined, tags combined] #=3
    # Hs is still a list of horizontal photos (aka slides) [ID, H, tags] #=3

    # allSlidesPossible = Hs | Vint  # union
    allSlidesPossible = Hs
    print "All possible slides = ", len(allSlidesPossible) + (len(vertical_images)/2)
    print len(Hs), "horizontals"
    print (len(vertical_images)/2, "vertical combinations")

    solution = solve1(Hs, vertical_images, dataset_letter)

    print "Solution complete... "
    print "Number of slides: ", len(solution.slides)
    print "Score: ", solution.get_score()

    print(solution.slides)

    solution.save_to_file()

    # outputName = "results/result-" + fn[0] + "-" + str(total) + ".txt"
    # with open(outputName, 'w') as f:
    #     for item in solution.slides:
    #         if type(item) is int:
    #             print >> f, item
    #         elif type(item[0]) is set:
    #             outlst = list(item[0])
    #             outstr = " ".join(str(x) for x in outlst)
    #             print >> f, outstr
    #         else:
    #             print >> f, item[0]
    #             if item[0] in VIDs:
    #                 print "ERROR: vertical ID alone"
    #
    # # create sets of all pictures
    # # create all combos of verticals together
    # # calculate all intersections and all disjoints
    # # 1 - put all horizontals together then match up verticals after
    # # 2 - start with one horizontal, pick next matching or +/- 1, continue
    # # 2a - start with horizontal, pick all matching int/dis as new branches
    #
    # total2 = validateScore(outputName, datafile)
    # print "Validated score from output file: ", total2
    #
    # if total == total2:
    #     print "\nCalculated score equals validated score from output file:", total, total2
    # else:
    #     print "\nScores do not match... shit's broke"

# D random Vs, 2, 1/2, 45 minutes, 205703
