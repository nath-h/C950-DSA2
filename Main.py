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

#(get_address_data())


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
#print(truck1)
truck2 = Truck(2, [2, 3, 4, 5, 7, 8, 10, 11, 12, 17, 18, 21, 22, 23, 36, 38], [], timedelta(hours=8, minutes=0, seconds=0), '', 0, True)
#print(truck2)
truck3 = Truck(3, [6, 9, 24, 25, 26, 27, 28, 32], [], timedelta(hours=9, minutes=30, seconds=0), '', 0, True)
#print(truck3)
truck4 = Truck(4, [1, 2, 3], [], timedelta(hours=8, minutes=0, seconds=0), '',   0, True)
### Package Requirements ###
'''
Truck1(departs 8am): 1, 13, 14, 15[priority 9am], 16, 19, 20, 29, 30, 31, 33, 34, 35, 37, 40 #Leave at 8am, package 15 deadline is 9am. Priority: 15, 1, 13, 14, 16, 20, 29, 30, 31, 34, 37, 40
 
Truck2(departs 8am): 2, 3, 4, 5, 7, 8, 10, 11, 12, 17, 18, 21, 22, 23, 36, 38 #Priority: None

Truck3(departs 9:05am): 6, 9, 24, 25, 26, 27, 28, 32, 39 Depart at 9:05am[delayed on flight] Priority: 6, 25. Save 9 for address update at 10:20am

Truck4(departs 8am, test): 1, 2, 3

# 36, 37

Package 1: Deadline: 10:30am 
Package 3: Must be on truck 2
Package 6: Delayed on flight: wll not arrive to depot until 905 am (will need to have a truck leave at 905) | Deadline: 1030am
Package 9: Wrong address (won't be updated until 10:20am)
Package 13: Deadline: 10:30am
Package 14: Must be delivered with package 15 and 19 | Deadline: 10:30am
Package 15: Deadline: 9:00am
Package 16: Must be delivered with package 13 and 19 | Deadline: 10:30am
Package 18: Must be on truck 2
Package 20: Must be delivered with package 13 and 15 | Deadline: 10:30am
Package 25: Delayed on flight: will not arrive to depot until 905 am (load on same truck as package 6) | Deadline: 10:30am
Package 28: Delayed on flight: will not arrive to depot until 905 am (load on same truck as packages 6 and 25)
Package 29: Deadline: 10:30am
Package 30: Deadline: 10:30am
Package 31: Deadline: 10:30am
Package 32: Delayed on flight: will not arrive to depot until 905 am (load on same truck as packages 6, 25, and 28)
Package 34: Deadline: 10:30am
Package 36: Must be on truck 2
Package 37: Deadline: 10:30am
Package 38: Must be on truck 2
Package 40: Deadline: 10:30am
'''
def load_packages(truck):
    truck.packages_on_truck = HashMap()
    for pkg in truck.packages:
      HashMap.add(truck.packages_on_truck, pkg, hash_map.get(pkg))

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
load_packages(truck4)
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

        if not truck.packages:
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
    delivery_algorithm(truck3, '4001 South 700 East', '4001 South 700 East')
print(round(truck1.miles_driven, 1), round(truck2.miles_driven, 1), round(truck3.miles_driven, 1), round(round(truck1.miles_driven, 1) + round(truck2.miles_driven, 1) + round(truck3.miles_driven, 1), 1))
tot_miles = truck1.miles_driven + truck2.miles_driven + truck3.miles_driven
print(round(tot_miles, 1))
print(truck1.current_time, truck2.current_time, truck3.current_time)
print(truck2.return_time)




hash_map.print()





