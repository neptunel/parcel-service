import datetime
# Class for Truck and truck functionalites
class Truck:

    def __init__(self, truck_id, departing_time):
        self.truck_id = truck_id
        self.avg_speed = 18
        self.max_capacity = 16
        self.packages = [] #stores the IDs of the packages
        self.total_miles = 0.0
        self.address = "4001 South 700 East"
        self.departing_time = departing_time
        self.total_time = departing_time
       
    # Load packages to packages list considering capacity limits
    def load_package_to_truck(self, package_id):
        if(len(self.packages) >= self.max_capacity):
            print("Truck is full and max capacity is 16, please don't load any packages to this truck anymore.")
        else:
            self.packages.append(package_id)

    # to print truck details
    def __str__(self):
        return (f"Truck ID: {self.truck_id} | "
                f"Packages: {[p for p in self.packages]}| "
                f"Departed at: {self.departing_time}| "
                f"Last Delivery Time: {self.total_time}| "
                f"Miles: {self.total_miles}\n")
