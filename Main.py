# Author: Fatma Sena Ekiz - Student ID: 011013854
import datetime, csv
from HashTable import HashTable
from Package import *
from Truck import *
import copy

# Load distances from distance_data.csv to a 2D array / matrix
def load_distance_matrix(file_path):
    with open(file_path, newline='') as csvfile:
        distance_matrix = list(csv.reader(csvfile))
    return distance_matrix
# Load address info from address_data.csv to a hash table usigng the index as key
def load_address_into_address_hash_table(file_path, hash_table):
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            index, location, address = row
            hash_table.insert(index, row)

# Return the package and truck indexes retrieved via lookup from the address hash table  
# Indexes are needed to get the distance between truck and package delivery locations
def find_address_indices(address_hash_table, truck_address, package_address=None):
    truck_location_index = 0
    package_address_index = 0
    i = 0

    while i < address_hash_table.size:
        data = address_hash_table.lookup(str(i))
        if data:
            if truck_address in data:
                truck_location_index = int(data[0])
            if package_address and package_address in data:
                package_address_index = int(data[0])
        i += 1
    
    return truck_location_index, package_address_index

#for each truck calculate the nearest neighbor to minimize the traveled distance
def deliver_using_nearest_neighbor(truck,package_hash_table,address_hash_table, distance_matrix ):
    # add package id's in the truck to list_of_truck_packages to be able to calculate nearest location per package later
    list_of_truck_packages =[]
    for id in truck.packages:
        package = package_hash_table.lookup(str(id))
        list_of_truck_packages.append(package)
 
    while(len(list_of_truck_packages) > 0):
        nearest_distance = 1000000000000.0 #Assign to a large value 
        nearest_package = None # Assign 'nearest_package to 'None'
        
        # Actual nearest neighbor algorithm starts here:
        # It measures the distance between each packages delivery address and the current location of the truck and delivers the closest package. 
        for package in list_of_truck_packages:
            truck_location_index, package_address_index = find_address_indices(address_hash_table, truck.address, package.address)

            # Retrieve the distance between current location and packages destination address
            if truck_location_index <= package_address_index:
                distance = float(distance_matrix[package_address_index][truck_location_index])
            else:
                distance = float(distance_matrix[truck_location_index][package_address_index])
            # Update nearest distance with minimum distance number each time
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_package = package
                
        # Loading and delivering the nearest package 
        list_of_truck_packages.remove(nearest_package)
        # add the chosen distance to the miles the truck has traveled
        truck.total_miles += nearest_distance
        # Set the truck address as the packages delivery address
        truck.address = nearest_package.address
        # Add the time travelled to the new package address, to the total truck travel time
        truck.total_time += datetime.timedelta(hours=nearest_distance / truck.avg_speed)
        # Set the new time to the packages delivery time
        nearest_package.delivery_time = truck.total_time
        nearest_package.departing_time = truck.departing_time

     # Return back to hub
    # If truck has no more packages and the first one completed delivery
    if len(list_of_truck_packages) > 0 and truck.departing_time == datetime.timedelta(hours=8):

        truck_location_index, _ = find_address_indices(address_hash_table, truck.address)
        # Gets the distance between the trucks current location and the hub
        distance = float(distance_matrix[truck_address_index][0])
        # Adds this time to the total miles traveled
        truck.total_miles += distance
        # Adds time traveled to hub to trucks time
        truck.total_time += datetime.timedelta(hours=distance / truck.avg_speed)

def setup_trucks(package_assignments, departure_times):
    """
    Setup trucks with assigned packages and departure times.
    
    Args:
        package_assignments (list of list of int): List containing package ID lists for each truck.
        departure_times (list of datetime.timedelta): List containing departure times for each truck.
    
    Returns:
        list of Truck: List of initialized Truck objects.
    """
    trucks = []
    for i, packages in enumerate(package_assignments):
        truck = Truck(str(i + 1), departure_times[i])
        for package_id in packages:
            truck.load_package_to_truck(package_id)
        trucks.append(truck)
    return trucks

def check_package_status(package_hash_table, time):

    package_id_input = input("Please enter the ID of the package to see status: ")
    if package_id_input.isdigit():
        package_id = str(package_id_input)
        package = package_hash_table.lookup(package_id)
        if package:
            package.update_package_status(time)
            print(package.__str__())
        else:
            print(f"No package found with ID {package_id}")
    else:
        print("Invalid input. Please enter a numeric package ID.")

def convert_to_timedelta(input_time):
    try:
        # Split the input time to separate the time and the AM/PM part
        time_part, am_pm = input_time.split(" ")

        # Split the time part into hours and minutes
        h, m = map(int, time_part.split(":"))

        # Convert hours to 24-hour format based on AM/PM
        if am_pm.upper() == 'PM' and h != 12:
            h += 12
        elif am_pm.upper() == 'AM' and h == 12:
            h = 0

        # Create the timedelta object
        time = datetime.timedelta(hours=h, minutes=m, seconds=0)
        return time
    except ValueError:
        print("Invalid time format. Please enter time in HH:MM AM/PM format.")
        return None

def show_menu():
    print("Please choose an operation:")
    print("1. Display Package Status")
    print("2. Display All Package Statuses")
    print("3. Display All Truck Details")
    print("4. Display Total Mileage")
    print("5. Exit")  

def main_menu(package_hash_table, trucks, total_miles, last_delivery_time):
    package_hash_table_backup = copy.deepcopy(package_hash_table)
    while True:
        package_hash_table = copy.deepcopy(package_hash_table_backup)
        show_menu()
        user_choice = input("Enter your choice: ")

        if user_choice == '1':
            input_time = input("Enter the time (HH:MM AM/PM) to check package status: ")
            
            time = convert_to_timedelta(input_time) 
            if time >= datetime.timedelta(hours=10, minutes=20, seconds=0):
                # Update incorrect address for package #9 at 10:20 AM
                package_hash_table.lookup('9').address = "410 S State St"
            check_package_status(package_hash_table, time)
        elif user_choice == '2':
            input_time = input("Enter the time (HH:MM AM/PM) to check package status: ")
            time = convert_to_timedelta(input_time) 
            if time >= datetime.timedelta(hours=10, minutes=20, seconds=0):
                # Update incorrect address for package #9 at 10:20 AM
                package_hash_table.lookup('9').address = "410 S State St"
            for id in range(1, 41):
                package = package_hash_table.lookup(str(id))
                package.update_package_status(time)
            package_hash_table.print()
        elif user_choice == '3':
            for truck in trucks:
                print(truck.__str__())
            print(f'Final Package Delivered at: {last_delivery_time}\n')
        elif user_choice == '4':
            print(f'Total Distance Covered: {round(total_miles, 2)} miles\n')
        elif user_choice == '5':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
def main():

    # Initialize the data from CSVs
    package_hash_table = HashTable()
    address_hash_table = HashTable()
   
    load_packages_into_package_hash_table('package_data.csv', package_hash_table)
    load_address_into_address_hash_table('address_data.csv', address_hash_table)
    distance_matrix = load_distance_matrix("distance_data.csv")

    print(f'\n Welcome to WGUPS Routing Program:')
    ascii_art = r"""

    _    _  _____  _   _ ______  _____   ______  _____  _   _  _____  _____  _   _  _____   ______ ______  _____  _____ ______   ___  ___  ___
    | |  | ||  __ \| | | || ___ \/  ___|  | ___ \|  _  || | | ||_   _||_   _|| \ | ||  __ \  | ___ \| ___ \|  _  ||  __ \| ___ \ / _ \ |  \/  |
    | |  | || |  \/| | | || |_/ /\ `--.   | |_/ /| | | || | | |  | |    | |  |  \| || |  \/  | |_/ /| |_/ /| | | || |  \/| |_/ // /_\ \| .  . |
    | |/\| || | __ | | | ||  __/  `--. \  |    / | | | || | | |  | |    | |  | . ` || | __   |  __/ |    / | | | || | __ |    / |  _  || |\/| |
    \  /\  /| |_\ \| |_| || |    /\__/ /  | |\ \ \ \_/ /| |_| |  | |   _| |_ | |\  || |_\ \  | |    | |\ \ \ \_/ /| |_\ \| |\ \ | | | || |  | |
    \/  \/  \____/ \___/ \_|    \____/   \_| \_| \___/  \___/   \_/   \___/ \_| \_/ \____/  \_|    \_| \_| \___/  \____/\_| \_|\_| |_/\_|  |_/
                                                                                                                                            
                                                                                                                                                                                                                                                                                
    """
    print(ascii_art)

    # Package assignments are done based on the requirements in package notes:
        # 3, 8, 36, 38 can only be in truck 2

        # 6, 25, 28, 32 are delayed on flight---will not arrive to depot until 9:05 am
        # so load them to second truck while first one is able to leave at 8am

        #packages below need to be delivered together and due to deadline they all loaded to truck 2
        # if package_id 14:
            #deliver with 15 and 19
        # if package_id 16:
            #deliver with 13 and 19
        # if package_id 20:
            #deliver with 13 and 15

    # Some packages have due dates, they need to leave early with loaded to truck 1

    package_assignments = [
    [1,13,14,15,16,20,29,30,31,34,37,40],
	[3,6,18,25,28,32,36,38,10,11,12,17,19],
	[2,4,5,7,8,9,10,21,22,23,24,26,27,33,35,39]
    ]

    departure_times = [
        datetime.timedelta(hours=8, minutes=0, seconds=0),
        datetime.timedelta(hours=9, minutes=5, seconds=0),
        datetime.timedelta(hours=10, minutes=20, seconds=0)
    ]

    # Initialize trucks and truck details
    trucks = setup_trucks(package_assignments, departure_times)
    total_miles =0
    last_delivery_time = 0

    # Simulate delivery using nearest neighbor algorithm

    for truck in trucks:
        deliver_using_nearest_neighbor(truck,package_hash_table,address_hash_table, distance_matrix )
        # Adds up total miles for printing to screen
        total_miles += truck.total_miles
        # Gets last delivery time for printing to screen
        last_delivery_time = truck.total_time
    
    #intuitive interface for the user to view the delivery status (including the delivery time) of any package at any time
    # and the total mileage traveled by all trucks. 

    main_menu(package_hash_table,trucks, total_miles, last_delivery_time)


if __name__ == "__main__":
    main()
       
       



       







  
   


        
