class SlideShow():
    def __init__(self, slides):
        assert (len(slides) > 1)
        self.slides = slides

    def score(self):
        score = 0
        for i in range(1, len(self.slides)):
            score += len(self.slides[i] - self.slides[i - 1])

        return score

    def __str__(self):
        result = str(len(self.slides)) + "\n"
        for slide in self.slides:
            result += str(slide.image1.id) + " "
            if (slide.image2 != None):
                result += str(slide.image2.id)
            result += "\n"
        return result

    def add_slide(self, slide):
        self.slides.append(slide)
