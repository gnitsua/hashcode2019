import scipy as scipy

from Slide import Slide
from constants import Orientation
from image import Image
from slideshow import SlideShow

from scipy.spatial import distance_matrix

if __name__ == "__main__":
    test1 = Image(1,"V",set({1,2,3}))
    test2 = Image(2,"V",set({3,4,53}))
    test3 = Image(3,"V",set({3,4,5}))
    slide = Slide(test1,test2)
    slide2 = Slide(test1,test3)
    # distance_matrix([test1,test2])

    # ss = SlideShow([slide,slide2])
    #
    #
    # print(ss.score())
    # print(ss)