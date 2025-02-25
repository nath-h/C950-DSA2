from datetime import *

class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, package_weight, delivery_status, package_notes ):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline if deadline else timedelta(hours=17, minutes=0, seconds=0)
        self.package_weight = package_weight
        self.delivery_status = delivery_status if delivery_status else 'At hub'
        self.package_notes = package_notes if package_notes else None
        self.delivery_time = None


    def __str__(self):
        return f"Package ID: {self.package_id}, Address: {self.address}, City: {self.city},  State: {self.state}, Zip Code: {self.zip_code}, Deadline: {self.deadline}, Package Weight: {self.package_weight}, Delivery Status: {self.delivery_status}, Package Notes: {self.package_notes} Delivered at: {self.delivery_time}"