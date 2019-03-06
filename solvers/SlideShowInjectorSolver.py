import os

import regex

from slideshow import SlideShow
from solvers.BaseSolver import Solver


class SlideShowInjectorSolver(Solver):
    filename_regex = regex.compile("(^result-)([a-e]{1})(-)(\d+)(.txt$)")

    def parse_filename(self, filename):
        if (regex.match(self.filename_regex, filename)):
            return {"dataset_letter": regex.match(self.filename_regex, filename).group(2),
                    "score": int(regex.match(self.filename_regex, filename).group(4))}
        else:
            raise AssertionError("Not all filenames are the right format")

    def solve(self):
        max_score = 0
        ss = None
        for filename in os.listdir("results"):
            try:
                parsed = self.parse_filename(filename)
                print(parsed)
                if (parsed["dataset_letter"] == self.dataset.dataset_letter):
                    score = parsed["score"]
                    if (score > max_score):
                        max_score = score
                        with open("results/" + filename, "r") as file:
                            temp = file.read()
                            ss = SlideShow.fromString(temp, self.dataset)
            except AssertionError:
                print("not a valid filename ({})".format(filename))
        if (ss != None):
            print("adding")
            print(ss.__str__(pretty=True))
            self.validate(ss)
        else:
            print("no valid slideshow for {}".format(self.dataset.dataset_letter))
        return ss
