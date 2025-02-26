from datetime import timedelta

#Package object constructor
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
        self.truck_id = 0
        self.deadline_delta = None
        self.departure_time = None

    #Method to print the object in string format
    def __str__(self):
        return f"Package ID: {self.package_id}, Address: {self.address}, City: {self.city},  State: {self.state}, Zip Code: {self.zip_code}, Deadline: {self.deadline}, Package Weight: {self.package_weight}, Delivery Status: {self.delivery_status}, Package Notes: {self.package_notes} Departed at: {self.departure_time}, Delivered at: {self.delivery_time}, Truck ID: {self.truck_id}"

    #Converts the deadline of packages to a timedelta for comparison later
    def convert_deadline(self):
        if self.deadline == "EOD":
            self.deadline_delta = timedelta(hours=17, minutes=0, seconds=0)  # 5:00 PM
        else:
            # Define time_conversion within this method
            def time_conversion(time_str):
                #Remove AM or PM from string and map the left side of : to hours and right side to minutes
                if "AM" in time_str or "PM" in time_str:
                    time_part = time_str.replace("AM", "").replace("PM", "").strip()
                    hours, minutes = map(int, time_part.split(":"))

                    #Convert 12 AM to 0 hours since 12:00 would be PM
                    if "AM" in time_str and hours == 12:
                        hours = 0
                    #Add 12 hours for PM times (except 12 PM)
                    elif "PM" in time_str and hours != 12:
                        hours += 12

                    return timedelta(hours=hours, minutes=minutes)
                else:
                    #If there's no AM or PM, time is handled here
                    time_parts = time_str.split(":")
                    hours = int(time_parts[0])
                    minutes = int(time_parts[1])

                    #Check if seconds are provided, otherwise set to 0
                    seconds = 0
                    if len(time_parts) == 3:
                        seconds = int(time_parts[2])

                    return timedelta(hours=hours, minutes=minutes, seconds=seconds)

            self.deadline_delta = time_conversion(self.deadline)
        return self.deadline_delta