from hashcode2018.Map import Map
from hashcode2018.Ride import Ride
class InputFile():
    def __init__(self, filename):
        with open(filename,"r") as file:
            map = Map.fromHeaderString(next(file))
            rides = []
            for ride_number,line in enumerate(file):
                rides.append(Ride.stringToRide(ride_number,line.strip('\n')))
        self.map = map
        self.rides = rides
