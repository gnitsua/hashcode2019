import numpy as np
class Ride():
    def __init__(self, start_row, start_col, end_row, end_col, earliest_start, latest_finish, number):
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col
        self.earliest_start = earliest_start
        self.latest_finish = latest_finish
        self.vehicle = None
        self.start = None
        self.finish = None
        self.number = number

    @classmethod
    def stringToRide(cls, line_number, string):
        split_string = string.split(" ")
        assert (len(split_string) == 6)
        try:
            start_row = int(split_string[0])
            start_col = int(split_string[1])
            end_row = int(split_string[2])
            end_col = int(split_string[3])
            earliest_start = int(split_string[4])
            latest_finish = int(split_string[5])
            return cls(start_row, start_col, end_row, end_col, earliest_start, latest_finish,line_number)
        except ValueError as e:
            raise AssertionError("invalid input")

    def show(self, ax):
        row_steps = list(range(min(self.start_row, self.end_row),max(self.start_row, self.end_row)+1))
        col_steps = list(range(min(self.start_col, self.end_col),max(self.start_col, self.end_col)+1))

        if (len(row_steps) > 0 and len(col_steps) > 0):
            if (len(row_steps) > len(col_steps)):
                col_steps = col_steps + [col_steps[-1]] * (len(row_steps) - len(col_steps))
            elif (len(row_steps) < len(col_steps)):
                row_steps = row_steps + [row_steps[-1]] * (len(col_steps) - len(row_steps))
            else:
                pass
        c = np.array(np.random.rand(3, 1) * 255).astype(int)
        ax.plot(row_steps, col_steps,  'o-',c)

    def __str__(self):
        return "%i(%i,%i)->(%i,%i)"%(self.number,self.start_row,self.start_col,self.end_row,self.end_col)
