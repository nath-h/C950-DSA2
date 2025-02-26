'''from datetime import timedelta


def time_conversion(time_requested):
    (h, m, s) = time_requested.split(":")
    h = int(h)
    m = int(m)
    s = int(h)
    return timedelta(hours=h, minutes=m, seconds=s)
#Prompt user for input:
print("Please pick an option for what you would like displayed:")
print("[1] Print a single package")
print("[2] Print all packages")
print("[0] Exit the program \n")
user_input = int(input())
if user_input == 0:
    print("Exiting program. Thank you!")

if user_input == 1:
    time_requested = input("Please enter a time, using the format HH:MM:SS: ")
    convert_time = time_conversion(time_requested)
    find_package_id = int(input("Enter package ID: "))
    package = hash_map.get(find_package_id)
    package.user_lookup(package)
if user_input == 2:
    print("2")'''