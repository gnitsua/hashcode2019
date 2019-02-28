class Map():
    def __init__(self,rows, columns, vehicles,rides,bonus,steps):
        self.rows = rows
        self.columns = columns
        self.vehicles = vehicles
        self.rides = rides
        self.bonus = bonus
        self.steps = steps

    @classmethod
    def fromHeaderString(cls,header_string):
        split_string = header_string.split(" ")
        assert(len(split_string) == 6)
        try:
            rows = int(split_string[0])
            columns = int(split_string[1])
            vehicles = int(split_string[2])
            rides = int(split_string[3])
            bonus = int(split_string[4])
            steps = int(split_string[5])

            return cls(rows,columns,vehicles,rides,bonus,steps)
        except ValueError as e:
            raise AssertionError("invalid header string")
