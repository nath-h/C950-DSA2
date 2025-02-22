from datetime import timedelta

from Packages import *
from HashMap import *
from csvreader import *

class Truck:
    def __init__(self, truck_id, packages, departure_time, return_time, miles_driven, at_hub):
        self.truck_id = truck_id
        self.packages = packages
        self.departure_time = departure_time if departure_time else timedelta(hours=8, minutes=0, seconds=0)
        self.return_time = return_time if return_time else timedelta(hours=17, minutes=0, seconds=0)
        self.miles_driven = miles_driven if miles_driven else 0
        self.speed = 18
        self.max_packages = 16
        self.hub_address = "4001 South 700 East"
        self.at_hub = at_hub if at_hub else False
        self.time = timedelta(hours=8, minutes=0, seconds=0)

    def __str__(self):
        return f"Truck id: {self.truck_id}, Packages: {self.packages}, Departure time: {self.departure_time}, Return time: {self.return_time}, Miles driven: {self.miles_driven}, Speed: {self.speed} mph, Max packages: {self.max_packages}, Hub address: {self.hub_address}, At hub: {self.at_hub}, Time: {self.time}"