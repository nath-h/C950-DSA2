import Truck
from HashMap import *
from Packages import *
from Truck import *
from csvreader import *
truck1 = Truck(1, [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 33, 34, 35, 37, 39, 40], [], timedelta(hours=8, minutes=0, seconds=0), '',   0, True)
print(truck1)
truck2 = Truck(2, [2, 3, 4, 5, 7, 8, 10, 11, 12, 17, 18, 21, 22, 23, 36, 38], [], timedelta(hours=8, minutes=0, seconds=0), '', 0, True)
print(truck2)
truck3 = Truck(3, [6, 9, 24, 25, 26, 27, 28, 32], [], timedelta(hours=9, minutes=5, seconds=0), '', 0, True)
print(truck3)
### Package Requirements ###
'''
Truck1(departs 8am): 1, 13, 14, 15[priority 9am], 16, 19, 20, 29, 30, 31, 33, 34, 35, 37, 40 #Leave at 8am, package 15 deadline is 9am. Priority: 15, 1, 13, 14, 16, 20, 29, 30, 31, 34, 37, 40
 
Truck2(departs 8am): 2, 3, 4, 5, 7, 8, 10, 11, 12, 17, 18, 21, 22, 23, 36, 38 #Priority: None

Truck3(departs 9:05am): 6, 9, 24, 25, 26, 27, 28, 32, 39 Depart at 9:05am[delayed on flight] Priority: 6, 25. Save 9 for address update at 10:20am

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

load_packages(truck1)
load_packages(truck2)
load_packages(truck3)
#truck1.packages_on_truck.print()
#deliver_package(truck1, 1)
#truck1.packages_on_truck.print()
def delivery_algorithm(truck):
    for package_id in truck.packages:
            package_info = truck.packages_on_truck.get(package_id)
            print(package_info.package_weight)




delivery_algorithm(truck1)
delivery_algorithm(truck2)

















