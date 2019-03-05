from sortedcollections import OrderedSet

from Slide import Slide

class SlideShow():
    def __init__(self):
        self.internal_score = 0
        self.slides= OrderedSet()

    # def add_slide_ids_to_set(self, slide):
    #     self.slide_ids.update(set([slide.image1.id]))
    #     if (slide.image2 != None):
    #         self.slide_ids.update(set([slide.image2.id]))

    def score(self):
        return self.internal_score

    def __str__(self):
        result = str(len(self.slides)) + "\n"
        for slide in self.slides:
            result += str(slide.image1.id) + " "
            if (slide.image2 != None):
                result += str(slide.image2.id)
            result += "\n"
        return result

    def add_images(self, *args):
        slide = Slide(*args)
        self.add_slide(slide)

    def add_slide(self, slide):
        num_slides = len(self.slides)
        self.slides.add(slide)
        if(len(self.slides) != num_slides+1):
            raise (AttributeError("slide already in slideshow"))
        else:
            if(len(self.slides) > 1):
                self.internal_score += self.slides[-1]-self.slides[-2]

    def pop(self):
        self.internal_score -= self.slides[-1] - self.slides[-2]
        self.slides.remove(max(self.slides))
