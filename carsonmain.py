import numpy as np
import sys
import csv
import random

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
    while index < len(slideSets)-1:
        total += score(slideSets[index],slideSets[index+1])
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

def generateVslides(Vs):
    Vint = []
    IDsdone = set() # set of frozensets of used VID combinations
    for i in Vs:
        for j in Vs:
            iset = frozenset((i[0],j[0]))
            if i[0] == j[0]:
                pass
            elif iset in IDsdone:
                pass
            else:
                unioned = i[2].union(j[2])
                Vint.append([set((i[0], j[0])), 'V', unioned])
                IDsdone.add(iset)
    return Vint

def generateRandomVSlides(Vs):
    Vint = []
    random.shuffle(Vs)

    index = 0
    while index < len(Vs)-1:
        i = Vs[index]
        j = Vs[index+1]
        unioned = i[2].union(j[2])
        Vint.append([set((i[0],j[0])), 'V', unioned])
        index += 2
    return Vint

def removeID(gotIDs,slides):
    if type(gotIDs) is set:
        IDs = list(gotIDs)
    else:
        IDs = [gotIDs]

    deleteme = []

    Hs = []
    Vs = []
    for slide in slides:
        if type(slide[0]) is int:
            Hs.append(slide)
        else:
            Vs.append(slide)

    Hs.sort(key=lambda x: x[0])

    if len(IDs) == 1: # remove horizontal
        ID = IDs[0]
        index = 0
        for Hslide in Hs:
            if ID == Hslide[0]:
                deleteme.append(index)
            if ID < Hslide[0]:
                break # leave for loop
            index += 1
        for i in sorted(deleteme, reverse=True):
            del Hs[i]
    else: #remove verticals
        index = 0
        for slide in Vs:
            for ID in IDs:
                if ID in slide[0]:
                    deleteme.append(index)
            index += 1
        deletemeFixed = list(set(deleteme))
        for i in sorted(deletemeFixed, reverse=True):
            del Vs[i]
    recombine = Hs + Vs
    random.shuffle(recombine)
    return recombine

def solve1(Hs,Vs,allSlidesPossible):
    # pick a random H to start with
    # force search until a score >= SCOREX is found
    # add, remove ID, reset SCOREX, and repeat
    count = 0
    solution = [count]
    total = 0
    SCOREXinit = 5 # VARY ME

    random.seed()
    if len(Hs) != 0:
        start = random.choice(Hs) # VARY ME (?)
    else:
        start = random.choice(Vs)
    A = start

    # add A to solution
    count += 1
    solution[0] = count
    solution.append(A)
    allSlidesPossible = removeID(A[0],allSlidesPossible)


    B = random.choice(allSlidesPossible)

    while len(allSlidesPossible) > 0:
        ATTEMPTSX = len(allSlidesPossible) # VARY ME, large effect on score and time
        SCOREX = SCOREXinit
        attempts = 0
        while score(A[2],B[2]) < SCOREX:
            if attempts < ATTEMPTSX:
                attempts += 1
                B = random.choice(allSlidesPossible)
            else:
                SCOREX = SCOREX - 1
                attempts = 0 #COULD GO IN ORDER, WHEN CONTINUING, KEEP GOING IN A CIRCLE TO ALLOW FOR A HIGHER SCORE TO REAPPEAR
        count +=1
        solution[0] = count
        solution.append(B)
        total += score(A[2],B[2])
        allSlidesPossible = removeID(B[0],allSlidesPossible)
        if count % 100 == 0:
            if ATTEMPTSX != 0:
                print total, " / #", count, " / ", len(allSlidesPossible), " left / ", 100*(float(attempts)/float(ATTEMPTSX)), "% tried"
        if len(allSlidesPossible) > 0:
            A = B
            B = random.choice(allSlidesPossible)

    return total,solution



if __name__ == "__main__":

    ##### READ DATA #####
    #fn = "a_example.txt"
    #fn = "b_lovely_landscapes.txt" # all horizontal
    fn = "c_memorable_moments.txt"
    #fn = "d_pet_pictures.txt"
    #fn = "e_shiny_selfies.txt"
    datafile = "data_sets/" + fn
    data = parseFile(datafile) #[ID, V/H, {tags}]
    print "Read ", len(data), " lines from data file: ", datafile

    ##### SEPARATE RAW DATA INTO Vs and Hs #####
    Vs = []
    Hs = []
    for i in data:
        if i[1] == "V":
            Vs.append(i)
        else:
            Hs.append(i)

    VIDs = [item[0] for item in Vs]

    ##### GENERATE ALL POSSIBLE VERTICALS #####
    print "Generating verticals from ", len(Vs), " vertical pictures"

    print "Generating ALL..."
    Vint = generateVslides(Vs) # okay for low numbers of verticals, 500 works
#OR VARY
    #print "Generating randoms..."
    #Vint = generateRandomVSlides(Vs)

    print "Calculated vertical combos... (", len(Vint), ")"
    # Vint is a list of all possible vertical combos (aka slides) [{ID1, ID2}, # of tags combined, tags combined] #=3
    # Hs is still a list of horizontal photos (aka slides) [ID, H, tags] #=3

    allSlidesPossible = Hs + Vint
    print "All possible slides = ", len(allSlidesPossible)
    print len(Hs), "horizontals"
    print len(Vint), "vertical combinations"

    total,solution = solve1(Hs,Vint,allSlidesPossible)

    print "Solution complete... "
    print "Number of slides: ", len(solution)-1
    print "Score: ", total

    outputName = "carsonResults/result-" + fn[0] + "-" + str(total) + ".txt"
    with open(outputName, 'w') as f:
        for item in solution:
            if type(item) is int:
                print >> f, item
            elif type(item[0]) is set:
                outlst = list(item[0])
                outstr = " ".join(str(x) for x in outlst)
                print >> f, outstr
            else:
                print >> f, item[0]
                if item[0] in VIDs:
                    print "ERROR: vertical ID alone"

    # create sets of all pictures
    # create all combos of verticals together
    # calculate all intersections and all disjoints
    # 1 - put all horizontals together then match up verticals after
    # 2 - start with one horizontal, pick next matching or +/- 1, continue
    # 2a - start with horizontal, pick all matching int/dis as new branches

    total2 = validateScore(outputName,datafile)
    print "Validated score from output file: ", total2

    if total == total2:
        print "\nCalculated score equals validated score from output file:", total, total2
    else:
        print "\nScores do not match... shit's broke"













# D random Vs, 2, 1/2, 45 minutes, 205703

