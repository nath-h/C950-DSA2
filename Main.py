# Name: Nathan Holman | Student ID: 012217520 | Program Mentor: Stephannie Schiro | Course Instructor: Elissa Thomas | Date: February 26, 2025

from datetime import datetime, timedelta
from Truck import *
import csv

hash_map = HashMap()
### LOAD CSV INFO ###
with open('WGUPS Package File.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    #For each package, create a new package object and add it to the hashmap
    for row in readCSV:
        package = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], None, row[7])
        hash_map.add(int(row[0]), package)


def get_address_data():
    addresses = []
    with open ('WGUPS addressCSV.csv') as csvfile:

        read_dist_csv = csv.reader(csvfile, delimiter=',')
        #Get the addresses only from the file instead of also getting the location name
        for row_idx, row in enumerate(read_dist_csv):
            address = row[2]
            #We don't need duplicate addresses, so skip if it is a duplicate
            if address not in addresses:
               addresses.append(address)
        return addresses

#Load 2d distance matrix data. We make sure we load these bidirectionally since the distance between
#address1 and address2 is the same
def get_distance_data():
    addresses = get_address_data()
    distance_data = {}

    for address in addresses:
        distance_data[address] = {}

    with open('WGUPS distanceCSV.csv') as csvfile:
        read_distance_csv = csv.reader(csvfile, delimiter=',')
        distance_matrix = list(read_distance_csv)

        row_count = min(len(distance_matrix), len(addresses))

        for row_idx in range(row_count):
            address_1 = addresses[row_idx]
            row = distance_matrix[row_idx]
            col_count = min(len(row), len(addresses))

            for col_idx in range(col_count):
                address_2 = addresses[col_idx]
                #We don't really need this check, but it's added for clarity. If there is no distance data, we assume
                #The distance is 0.0
                try:
                    distance_value = float(row[col_idx]) if row[col_idx] else 0.0
                except ValueError:
                    distance_value = 0.0

                # Store the distance
                distance_data[address_1][address_2] = distance_value

                # Bidirectional handling
                if address_1 != address_2:
                    if address_2 not in distance_data:
                        distance_data[address_2] = {}
                    distance_data[address_2][address_1] = distance_value

    return addresses, distance_data

#Calculates the distance between a starting address and the destination address
#Checks to make sure the addresses passed to it are in the distance data
def calculate_route(start_address, destination_address):
    addresses, distance_data = get_distance_data()

    if start_address not in distance_data:
        return f"Error: Start address '{start_address}' not found in distance data. Available addresses: {addresses}"

    if destination_address not in distance_data[start_address]:
        return f"Error: Destination address '{destination_address}' not found in distance data. Available addresses: {addresses}"

    distance = distance_data[start_address][destination_address]
    return f"TEST Distance from {start_address} to {destination_address}: {distance} miles TEST", distance


#Load the trucks and instantiate the objects
truck1 = Truck(1, [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 33, 34, 35, 37, 39, 40], [], timedelta(hours=8, minutes=0, seconds=0), '',   0, True)
truck2 = Truck(2, [2, 3, 4, 5, 7, 8, 10, 11, 12, 17, 18, 21, 22, 23, 36, 38], [], timedelta(hours=8, minutes=0, seconds=0), '', 0, True)
truck3 = Truck(3, [6, 9, 24, 25, 26, 27, 28, 32], [], timedelta(hours=9, minutes=5, seconds=0), '', 0, True)
#Above we manually insert package IDs into the truck, here we actually load the package data onto the truck using the packages list
#We also assign the truckID and departure time of the truck to each package
def load_packages(truck):
    truck.packages_on_truck = HashMap()
    for pkg in truck.packages:
        package_obj = hash_map.get(pkg)
        hash_map.get(pkg).departure_time = truck.departure_time
        HashMap.add(truck.packages_on_truck, pkg, package_obj)
        package_obj.truck_id = truck.truck_id


    return truck.packages_on_truck
#Takes a package_id and removes it from the truck
def deliver_package(truck, package_id):
    truck.packages.remove(package_id)
    truck.packages_on_truck.delete(package_id)

#Takes a distance, divides it by the speed to get amount of hours, then converts it to seconds for increased accuracy.
#Example: 10 miles drive, 20 miles per hour. .5 hours. 3600 seconds in an hour, .5 is 1800 seconds.
#1800 seconds * .5 hours = 30 minutes. Then returns the timedelta(we use this as elapsed time)
#In our example above, our return would be 00:30:00
def calculate_delivery_time(speed, distance):
    time_hours = distance / speed
    time_seconds = time_hours * 3600
    return timedelta(seconds=time_seconds)
#Load the trucks using the function defined above
load_packages(truck1)
load_packages(truck2)
load_packages(truck3)
#Core delivery algorithm that is called recursively.
def delivery_algorithm(truck, address1, address2):
    package_distances = {}
    #If no address is provided, the address is instantiated as the hub.
    address1 = address1 if address1 else truck.hub_address
    address2 = address2 if address2 else truck.hub_address
    #We use this current_location later to print distances from A to B. Although these are the same distance reversed,
    #We need to describe what order we are delivering packages.
    #We also use it to check special conditions for priority packages later so we can determine what address to deliver
    #to next.
    current_location = address1


    #If address1 and address2 are not BOTH the hub, this means we have a priority package. Process that package first, regardless of distance.
    if address1 or address2 == '4001 South 700 East' and address2 != address1:
        # Find package with address2
        priority_package_id = None
        for package_id in truck.packages:
            package_info = truck.packages_on_truck.get(package_id)
            if package_info and package_info.address == address2:
                priority_package_id = package_id
                break
        #Deliver the priority package
        if priority_package_id:
                _, distance = calculate_route(current_location, address2)
                print( f"Priority delivery - prioritizing package {priority_package_id} to {address2} with a distance of {distance}")
                time_elapsed = calculate_delivery_time(truck.speed, distance)
                truck.current_time += time_elapsed

                #Remove the delivered package
                current_package = truck.packages_on_truck.get(priority_package_id)
                deliver_package(truck, priority_package_id)
                current_package.delivery_status = 'Delivered'
                current_package.delivery_time = truck.current_time

                delivery_algorithm(truck, address2, address2)
                return

    #Calculate distance from current location to each remaining package address
    for package_id in truck.packages:
        package_info = truck.packages_on_truck.get(package_id)

        if package_info:
            _, distance = calculate_route(address1, package_info.address)
            package_distances[package_id] = distance

    # Find the package with minimum distance
    if package_distances:
        min_distance_package_id = min(package_distances, key=package_distances.get)
        min_distance_address = truck.packages_on_truck.get(min_distance_package_id).address
        min_distance = package_distances[min_distance_package_id]
        current_package = truck.packages_on_truck.get(min_distance_package_id)

        #Special condition for Package ID 9, don't update the package address until 10:20 AM.
        #We don't need to add any special logic for delivery because our algorithm already delivers it after 10:20 AM anyway.
        if truck.current_time >= timedelta(hours=10, minutes=20, seconds=0):
            package_9 = hash_map.get(9)
            if package_9 and package_9.address != '410 S State St':
                package_9.address = '410 S State St'
                package_9.zip_code = '84111'

        #We start truck3 at 5383 South 900 East #104 because it has a deadline of 10:30, and so does 3060 Lester St.
        #We first prioritize 5383 South 900 East #104 because it has the least distance from the hub. Next,
        #We deliver to 3060 Lester St to ensure we get packages delivered to both addresses before their deadline.
        if current_location == '5383 South 900 East #104':
            current_package.delivery_status = 'Delivered'
            current_package.delivery_time = truck.current_time
            deliver_package(truck, min_distance_package_id)

            if truck.packages:
                delivery_algorithm(truck, current_location, '3060 Lester St')
            return

        print(f"Delivering package {min_distance_package_id} from {address1} to {min_distance_address} with a distance of {min_distance}")

        #Update time
        time_elapsed = calculate_delivery_time(truck.speed, min_distance)
        truck.current_time += time_elapsed
        #We don't need to do this, however we convert EOD to be 5PM for sake of checking package deadlines.
        #We consider end of day deadline to be 5PM.
        time_str = current_package.deadline
        if time_str == 'EOD':
            time_str = '5:00 PM'
        time_obj = datetime.strptime(time_str, '%I:%M %p')

        #We convert our deadline string to a timedelta here for comparisons. If the time_delta(the deadline)
        #Is less than the truck.current_time, our package is late.
        time_delta = timedelta(hours=time_obj.hour, minutes=time_obj.minute, seconds=time_obj.second)
        if time_delta < truck.current_time:
            print(f"LATE PACKAGE {current_package}")

        #Update truck mileage
        truck.miles_driven += package_distances[min_distance_package_id]
        #Remove the delivered package
        current_package.delivery_status = 'Delivered'
        current_package.delivery_time = truck.current_time
        deliver_package(truck, min_distance_package_id)
        #Return to hub if truck is empty and calculate the distance to hub from our current address. We don't need
        #To return to the hub if our truck_id is 3 because our deliveries will be complete.
        if not truck.packages and truck.truck_id != 3:
            print("All done! Returning to hub")
            _, distance_to_hub = calculate_route(min_distance_address, '4001 South 700 East')
            print(f"Distance back to hub: {distance_to_hub}")
            truck.miles_driven += distance_to_hub
            time_elapsed = calculate_delivery_time(truck.speed, distance_to_hub)
            truck.current_time += time_elapsed
            truck.return_time = truck.current_time
            return

        #Continue with next delivery from the new location by recursively calling delivery_algorithm.
        delivery_algorithm(truck, min_distance_address, address2)
    else:
        print("All packages have been delivered. The day is complete.")



#Run delivery algorithm on our first two trucks. Since we have no priority, we start both addresses at the hub
#And let our algorithm find the best route
delivery_algorithm(truck1, '4001 South 700 East', '4001 South 700 East')
delivery_algorithm(truck2, '4001 South 700 East', '4001 South 700 East')
#Once truck1 is empty, we can send truck 3
if not truck1.packages:
    truck3.current_time = truck1.current_time
    truck3.departure_time = truck1.current_time
    for package in truck3.packages:
        package = hash_map.get(package)
        package.departure_time = truck3.current_time
    #5383 South 900 East has a 10:30 deadline so it's our priority delivery
    delivery_algorithm(truck3, '4001 South 700 East', '5383 South 900 East #104')

#Convert our user_input time to a timedelta to compare with package delivery deadline
def time_conversion(time_requested):
    #This handles deadline being in string format such as 10:30 AM
    if "AM" in time_requested:
        time_part = time_requested.replace("AM",  "").strip()
        hours, minutes = map(int, time_part.split(":"))
        return timedelta(hours=hours, minutes=minutes)
    #User input will be HH:MM:SS so we split it
    else:
        (h, m, s) = time_requested.split(":")
        h = int(h)
        m = int(m)
        s = int(s)
        return timedelta(hours=h, minutes=m, seconds=s)
#Prompt user for input and display total miles driven:
print(f"Total distance traveled by all trucks: Truck 1: {round(truck1.miles_driven,1)}, Truck 2: {round(truck2.miles_driven, 1)}, Truck 3: {round(truck3.miles_driven, 1)}, Total: {round(truck1.miles_driven + truck2.miles_driven + truck3.miles_driven, 1)}\n")
print("##### WGUPS Package Information System #####\n")
print("Please pick an option:")
print("[0] Exit the program")
print("[1] Print a single package")
print("[2] Print all packages\n")
#While True will run until the user quits the program. Otherwise, we will keep cycling through the options
while True:
    user_input = int(input())
    if user_input == 0:
        print("Exiting program. Thank you!")
        break
    #If the user selects 1, we will prompt them for a time and a package id in order to look up the requested information.
    if user_input == 1:
        time_requested = input("Please enter a time, using the format HH:MM:SS: ")
        convert_time = time_conversion(time_requested)
        find_package_id = int(input("Enter package ID: "))
        package = hash_map.get(find_package_id)
        #Handle lookup of package 9 given its constraints
        original_address = None
        original_zip = None
        time_threshold = timedelta(hours=10, minutes=20, seconds=0)
        if find_package_id == 9 or package.package_id == 9:
            package_9 = hash_map.get(9)
            original_address = package_9.address
            original_zip = package_9.zip_code
            #If it is before 10:20, give the incorrect address
            if convert_time < time_threshold:
                package_9.address = '300 State St'
                package_9.zip_code = '84103'
            #If it is after 10:20, give the correct address
            else:
                package_9.address = '410 S State St'
                package_9.zip_code = '84111'
        #If deadline_delta has not been converted yet, convert it so we can use our comparison operators.
        if package.deadline_delta is  None:
            package.convert_deadline()
        #The following checks compare the time given to our departure time and delivery time to determine whether
        #The package is at the hub, en route, or delivered. If this were a real world application we would have a check
        #For late packages as well, but we know we don't have those so we can skip it for simplicity.
        if convert_time > package.delivery_time:
         temp_status = "Delivered"
         print(f"Current information for Package ID: {package.package_id}, Truck ID: {package.truck_id} Time requested: {convert_time}, Delivery time: {package.delivery_time}, Delivery status: {temp_status} Package address: {package.address} {package.zip_code} {package.city} {package.state}")


        elif package.departure_time < convert_time < package.delivery_time:

            temp_status = "En route"
            print(f"Current information for Package ID: {package.package_id} Truck ID: {package.truck_id} Time requested: {convert_time}, Expected delivery time: {package.delivery_time}, Delivery status: {temp_status}, Deadline: {package.deadline_delta} Package address: {package.address} {package.zip_code} {package.city} {package.state}")


        elif convert_time <= package.departure_time:
            temp_status = "At hub"
            print(f"Current information for Package ID: {package.package_id} Truck ID: {package.truck_id} Time requested: {convert_time}, Expected departure time: {package.departure_time}, Expected delivery time: {package.delivery_time}, Current status: {temp_status}, Deadline: {package.deadline_delta} Package address: {package.address} {package.zip_code} {package.city} {package.state}")




    #If the user input is 2, we will do something similar to what we've done above, however we will instead iterate
    #Through all packages. Much of this code is reused from above so only new code will be commented.
    elif user_input == 2:
        time_requested = input("Please enter a time, using the format HH:MM:SS:")
        convert_time = time_conversion(time_requested)
        #Iterate through all packages, and do the same as above.
        for package_id in range(1, 41):
            package = hash_map.get(package_id)
            #Handle the special case of package 9 based off the user inputted time
            time_threshold = timedelta(hours=10, minutes=20, seconds=00)
            if package_id == 9:
                if convert_time < time_threshold:
                    temp_address = package.address
                    temp_zip = package.zip_code
                    package.address = '300 State St'
                    package.zip_code = '84103'
                else:
                    package.address = '410 S State St'
                    package.zip_code = '84111'


            if package.deadline_delta is None:
                package.convert_deadline()
            if convert_time > package.delivery_time:
                #We use a temp_status here because we want we are iterating through all packages instead of just checking
                #One package. We want our information at time_requested to show a different result than our final status (if they are different)
                #We will use this temp_status below as well for en route and at hub
                temp_status = "Delivered"

            elif package.departure_time < convert_time < package.delivery_time:
                temp_status = "En route"

            elif convert_time < package.departure_time:
                temp_status = "At hub"
            print(f"Package ID: {package.package_id} Truck ID: {package.truck_id} Time requested: {convert_time}, Expected departure time: {package.departure_time}, Expected delivery time: {package.delivery_time}, Current status: {temp_status}, Deadline: {package.deadline_delta} Package address: {package.address} {package.zip_code} {package.city} {package.state}")


    else: print("Invalid option. Please pick 0, 1, or 2.\n")

    print( f"\nTotal distance traveled by all trucks: Truck 1: {round(truck1.miles_driven, 1)}, Truck 2: {round(truck2.miles_driven, 1)}, Truck 3: {round(truck3.miles_driven, 1)}, Total: {round(truck1.miles_driven + truck2.miles_driven + truck3.miles_driven, 1)}\n")
    print("Please pick an option:")
    print("[0] Exit the program")
    print("[1] Print a single package")
    print("[2] Print all packages\n")