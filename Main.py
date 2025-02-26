# Name: Nathan Holman | Student ID: 012217520 | Program Mentor: Stephannie Schiro | Course Instructor: Elissa Thomas | Date: February 26, 2025

from datetime import datetime, timedelta
import Truck
from HashMap import *
from Packages import *
from Truck import *
from csvreader import *
import csv

### LOAD CSV ###

hash_map = HashMap()
with open('WGUPS Package File.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')

    for row in readCSV:
        package = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], None, row[7])
        hash_map.add(int(row[0]), package)
        #print(package)



def get_address_data():
    addresses = []
    with open ('WGUPS addressCSV.csv') as csvfile:


        read_dist_csv = csv.reader(csvfile, delimiter=',')



        for row_idx, row in enumerate(read_dist_csv):
            address = row[2]
            if address not in addresses:
               addresses.append(address)
        return addresses




def get_distance_data():
    addresses = get_address_data()
    distance_data = {}

    # Initialize the dictionary for all addresses
    for address in addresses:
        distance_data[address] = {}

    with open('WGUPS distanceCSV.csv') as csvfile:
        read_distance_csv = csv.reader(csvfile, delimiter=',')
        distance_matrix = list(read_distance_csv)

        # Process the distance matrix
        row_count = min(len(distance_matrix), len(addresses))

        for row_idx in range(row_count):
            address_1 = addresses[row_idx]
            row = distance_matrix[row_idx]

            col_count = min(len(row), len(addresses))

            for col_idx in range(col_count):
                address_2 = addresses[col_idx]

                try:
                    distance_value = float(row[col_idx]) if row[col_idx] else 0.0
                except ValueError:
                    distance_value = 0.0

                # Store the distance
                distance_data[address_1][address_2] = distance_value

                # Store the same distance in the opposite direction to ensure symmetry
                if address_1 != address_2:  # Skip if it's the same address
                    if address_2 not in distance_data:
                        distance_data[address_2] = {}
                    distance_data[address_2][address_1] = distance_value

    return addresses, distance_data



def calculate_route(start_address, destination_address):
    addresses, distance_data = get_distance_data()


    if start_address not in distance_data:
        return f"Error: Start address '{start_address}' not found in distance data. Available addresses: {addresses}"

    if destination_address not in distance_data[start_address]:
        return f"Error: Destination address '{destination_address}' not found in distance data. Available addresses: {addresses}"

    distance = distance_data[start_address][destination_address]
    return f"TEST Distance from {start_address} to {destination_address}: {distance} miles TEST", distance


### LOAD TRUCKS ###
truck1 = Truck(1, [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 33, 34, 35, 37, 39, 40], [], timedelta(hours=8, minutes=0, seconds=0), '',   0, True)
truck2 = Truck(2, [2, 3, 4, 5, 7, 8, 10, 11, 12, 17, 18, 21, 22, 23, 36, 38], [], timedelta(hours=8, minutes=0, seconds=0), '', 0, True)
truck3 = Truck(3, [6, 9, 24, 25, 26, 27, 28, 32], [], timedelta(hours=9, minutes=5, seconds=0), '', 0, True)

def load_packages(truck):
    truck.packages_on_truck = HashMap()
    for pkg in truck.packages:
        package_obj = hash_map.get(pkg)
        if package_obj.deadline_delta is None:
            package_obj.convert_deadline()
        hash_map.get(pkg).delivery_status = "En route"
        hash_map.get(pkg).departure_time = truck.departure_time
        HashMap.add(truck.packages_on_truck, pkg, package_obj)
        package_obj.truck_id = truck.truck_id


    return truck.packages_on_truck

def deliver_package(truck, package_id):
    truck.packages.remove(package_id)
    truck.packages_on_truck.delete(package_id)


def calculate_delivery_time(speed, distance):
    time_hours = distance / speed
    time_seconds = time_hours * 3600
    return timedelta(seconds=time_seconds)



load_packages(truck1)
load_packages(truck2)
load_packages(truck3)
#load_packages(truck4)
#truck1.packages_on_truck.print()
#deliver_package(truck1, 1)
#truck1.packages_on_truck.print()




def delivery_algorithm(truck, address1, address2):
    package_distances = {}
    address1 = address1 if address1 else truck.hub_address
    address2 = address2 if address2 else truck.hub_address
    current_location = address1
    # If no packages left, return


    if address1 or address2 == '4001 South 700 East' and address2 != address1:
        # Find package with address2
        first_package_id = None
        for package_id in truck.packages:
            package_info = truck.packages_on_truck.get(package_id)
            if package_info and package_info.address == address2:
                first_package_id = package_id
                break

        if first_package_id:
                _, distance = calculate_route(current_location, address2)
                print( f"First delivery - prioritizing package {first_package_id} to {address2} with a distance of {distance}")
                time_elapsed = calculate_delivery_time(truck.speed, distance)
                truck.current_time += time_elapsed
                print(truck.current_time)
                print(time_elapsed)

                # Update truck mileage
                #truck.mileage += distance

                # Remove the delivered package
                current_package = truck.packages_on_truck.get(first_package_id)
                deliver_package(truck, first_package_id)
                current_package.delivery_status = 'Delivered'
                current_package.delivery_time = truck.current_time


                delivery_algorithm(truck, address2, address2)
                return

    # Calculate distance from current location to each package address
    for package_id in truck.packages:
        package_info = truck.packages_on_truck.get(package_id)

        if package_info:
            # Get distance info from calculate_route
            _, distance = calculate_route(address1, package_info.address)
            # Store package_id and its distance
            package_distances[package_id] = distance

    # Find the package with minimum distance
    if package_distances:
        min_distance_package_id = min(package_distances, key=package_distances.get)
        min_distance_address = truck.packages_on_truck.get(min_distance_package_id).address
        min_distance = package_distances[min_distance_package_id]
        current_package = truck.packages_on_truck.get(min_distance_package_id)
        print(current_package.package_id)
        print(current_package.address)

        if truck.current_time >= timedelta(hours=10, minutes=20, seconds=0):
            package_9 = hash_map.get(9)
            if package_9 and package_9.address != '410 S State St':
                package_9.address = '410 S State St'
                package_9.zip_code = '84111'


        if current_location == '5383 South 900 East #104':
            current_package.delivery_status = 'Delivered'
            current_package.delivery_time = truck.current_time
            deliver_package(truck, min_distance_package_id)

            if truck.packages:
                delivery_algorithm(truck, current_location, '3060 Lester St')
            return







        print(f"Delivering package {min_distance_package_id} from {address1} to {min_distance_address} with a distance of {min_distance}")

        # Update time
        time_elapsed = calculate_delivery_time(truck.speed, min_distance)
        truck.current_time += time_elapsed
        #print(current_package.deadline)
        time_str = current_package.deadline
        if time_str == 'EOD':
            time_str = '5:00 PM'
        time_obj = datetime.strptime(time_str, '%I:%M %p')
        time_delta = timedelta(hours=time_obj.hour, minutes=time_obj.minute, seconds=time_obj.second)
        if time_delta < truck.current_time:
            print(f"LATE PACKAGE {current_package}")


        # Update truck mileage
        truck.miles_driven += package_distances[min_distance_package_id]

        # Remove the delivered package
        current_package.delivery_status = 'Delivered'
        current_package.delivery_time = truck.current_time
        deliver_package(truck, min_distance_package_id)

        if not truck.packages and truck.truck_id != 3:
            print("All done! Returning to hub")
            _, distance_to_hub = calculate_route(min_distance_address, '4001 South 700 East')
            print(f"Distance back to hub: {distance_to_hub}")
            truck.miles_driven += distance_to_hub
            time_elapsed = calculate_delivery_time(truck.speed, distance_to_hub)
            truck.current_time += time_elapsed
            truck.return_time = truck.current_time
            return

        # Continue with next delivery from the new location
        delivery_algorithm(truck, min_distance_address, address2)
        #hash_map.print()
    else:
        print("No valid packages to deliver")




delivery_algorithm(truck1, '4001 South 700 East', '4001 South 700 East')
delivery_algorithm(truck2, '4001 South 700 East', '4001 South 700 East')
print(truck2.packages)
if not truck1.packages:
    truck3.current_time = truck1.current_time
    print(truck3.departure_time)
    delivery_algorithm(truck3, '4001 South 700 East', '5383 South 900 East #104')
print(round(truck1.miles_driven, 1), round(truck2.miles_driven, 1), round(truck3.miles_driven, 1), round(round(truck1.miles_driven, 1) + round(truck2.miles_driven, 1) + round(truck3.miles_driven, 1), 1))
tot_miles = truck1.miles_driven + truck2.miles_driven + truck3.miles_driven
print(round(tot_miles, 1))
print(truck1.current_time, truck2.current_time, truck3.current_time)
print(truck2.return_time)




hash_map.print()
def time_conversion(time_requested):
    if "AM" in time_requested:
        time_part = time_requested.replace("AM",  "").strip()  # Get "10:30"
        hours, minutes = map(int, time_part.split(":"))
        return timedelta(hours=hours, minutes=minutes)
    else:
        (h, m, s) = time_requested.split(":")
        h = int(h)
        m = int(m)
        s = int(s)
        return timedelta(hours=h, minutes=m, seconds=s)
#Prompt user for input:
print(f"Total distance traveled by all trucks: Truck 1: {round(truck1.miles_driven,1)}, Truck 2: {round(truck2.miles_driven, 1)}, Truck 3: {round(truck3.miles_driven, 1)}, Total: {round(tot_miles, 1)}")
print("Please pick an option:")
print("[0] Exit the program")
print("[1] Print a single package")
print("[2] Print all packages\n")
while True:
    user_input = int(input())
    if user_input == 0:
        print("Exiting program. Thank you!")
        break

    if user_input == 1:
        time_requested = input("Please enter a time, using the format HH:MM:SS: ")
        convert_time = time_conversion(time_requested)
        find_package_id = int(input("Enter package ID: "))
        package = hash_map.get(find_package_id)
        if package.deadline_delta is  None:
            package.convert_deadline()
        if convert_time > package.delivery_time:
         temp_status = "Delivered"
         print(f"Time requested: {convert_time}, Delivery time: {package.delivery_time}, Delivery status: {temp_status}")
         print(f"Final status: {hash_map.get(find_package_id)}\n")

        elif package.departure_time < convert_time < package.delivery_time:

            package.delivery_status = "En route"
            print(f"Time requested: {convert_time}, Expected delivery time: {package.delivery_time}, Delivery status: {temp_status}, Deadline: {package.deadline_delta}")
            print(f"Final status: {hash_map.get(find_package_id)}\n")

        elif convert_time < package.departure_time:
            temp_status = "At hub"
        print(f"Information for Package ID: {package.package_id} Time requested: {convert_time}, Expected departure time: {package.departure_time}, Expected delivery time: {package.delivery_time}, Current status: {temp_status}, Deadline: {package.deadline_delta}")
        print(f"Final status: {hash_map.get(find_package_id)}\n")




    elif user_input == 2:
        time_requested = input("Please enter a time, using the format HH:MM:SS:")
        convert_time = time_conversion(time_requested)
        package_9 = hash_map.get(9)
        if convert_time < timedelta(hours=10, minutes=20, seconds=0):
            package_9.address = "300 State St"
            package_9.zip_code = "84103"
        else:
            package_9.address = "410 S State St"
            package_9.zip_code = "84111"
        for package_id in range(1, 41):
            #convert_time = time_conversion(time_requested)
            package = hash_map.get(package_id)
            if package.deadline_delta is None:
                package.convert_deadline()
            if convert_time > package.delivery_time:
                temp_status = "Delivered"
              #  print(f"Time requested: {convert_time}, Delivery time: {package.delivery_time}, Delivery status: {package.delivery_status}")
               # print(f"Final status: {hash_map.get(package_id)}")


            elif package.departure_time < convert_time < package.delivery_time:
                temp_status = "En route"
               # print(f"Time requested: {convert_time}, Expected delivery time: {package.delivery_time}, {package.delivery_status}, Deadline: {package.deadline_delta}")
               # print(f"Final status: {hash_map.get(package_id)}")

            elif convert_time < package.departure_time:
                temp_status = "At hub"
               # print(f"Time requested: {convert_time}, Expected departure time: {package.departure_time}, Expected delivery time: {package.delivery_time}, Current status: {package.delivery_status}, Deadline: {package.deadline_delta}")
            print(f"Package ID: {package.package_id} Time requested: {convert_time}, Expected departure time: {package.departure_time}, Expected delivery time: {package.delivery_time}, Current status: {temp_status}, Deadline: {package.deadline_delta}")
            print(f"Final status: {hash_map.get(package_id)}\n")

    else: print("Invalid option. Please pick 0, 1, or 2.\n")

    print("Please pick an option:")
    print("[0] Exit the program")
    print("[1] Print a single package")
    print("[2] Print all packages\n")







#package.user_lookup(1)

#hash_map.print()
print(hash_map.get(1))