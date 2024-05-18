# Class for Truck and truck functionalites
class Truck:

    def __init__(self, packages, depart_time):
        self.capacity = 16
        self.speed = 18
        self.packages = packages
        self.miles = 0.0
        self.address = "4001 South 700 East"
        self.depart_time = depart_time
        self.time = depart_time

    def __str__(self):
        return f'{str(self.packages)}'