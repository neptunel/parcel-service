import csv
from HashTable import HashTable
# Class for Package and package functionalities
class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, special_note):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.special_note = special_note or "N/A"
        self.status = "At the Hub"
        self.delivery_time = None
        self.departing_time = None
        

    def update_package_status(self, input_time):
        if input_time > self.delivery_time:
            self.status = 'Delivered'
        elif self.departing_time > input_time:
            self.status = 'En Route'
        else:
            self.status = 'At the Hub'

    def __str__(self):
        return (f"Package ID: {self.package_id} | "
                f"Address: {self.address}, {self.city},{self.state},{self.zip_code} | "
                f"Deadline: {self.deadline} | "
                f"Weight: {self.weight}kg | "
                f"Status: {self.status} | "
                f"Delivery Time: {self.delivery_time} | "
                f"Special Note: {self.special_note}\n")

def load_packages_into_package_hash_table(file_path, hash_table):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            package_id, address, city, state, zip_code, deadline, weight, special_note = row
            packages = Package(package_id, address, city, state, zip_code, deadline, weight,special_note)
            hash_table.insert(package_id, packages)
        
