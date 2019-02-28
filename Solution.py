import Ride
import matplotlib.pyplot as plt


class Solution():
    def __init__(self,map):
        self.rides = []
        self.map = map

    def addRide(self,ride:Ride):
        self.rides.append(ride)

    def show(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for ride in self.rides:
            ride.show(ax)
        ax.set_ylim([0,self.map.rows])
        ax.set_xlim([0,self.map.columns])
        ax.grid(True)
        plt.show()


    def __str__(self):
        vehicles = {}
        for ride in self.rides:
            if(ride.vehicle not in vehicles):
                vehicles[ride.vehicle] = []
                vehicles[ride.vehicle].append(ride.number)
            else:
                vehicles[ride.vehicle].append(ride.number)
        print(vehicles)
        result = ""
        for vehicle_number,rides in vehicles.items():
            result = result+str(vehicle_number)+" "+" ".join(str(x) for x in rides)+"\n"
        return result