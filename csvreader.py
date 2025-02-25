'''
import csv
from HashMap import *
from Packages import *
hash_map = HashMap()
with open('WGUPS Package File.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')

    for row in readCSV:
        package = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], None, row[7])
        hash_map.add(int(row[0]), package)
        print(package)





#######distance table reader########
addresses = []
def get_distance2(address1, address2):
    addresses = []
    distance_matrix = []
    with open ('WGUPS addressCSV.csv') as csvfile:
      read_dist_csv = list(csv.reader(csvfile, delimiter=','))
    addresses = read_dist_csv[0]


    for row, row_idx in enumerate(read_dist_csv):
         addresses.append(row_idx[1])

print(addresses)
def get_distance(address1, address2):
    addresses = []
    distance_matrix = []
    with open('WGUPS distanceCSV.csv') as csvfile:
     read_distance_csv = list(csv.reader(csvfile, delimiter=','))
    addresses = read_distance_csv[0]
    distance_matrix = read_distance_csv[1:]
    try:
        index_1 = addresses.index(address1)
        index_2 = addresses.index(address2)
    except ValueError:
        return f"Error: One or both addresses not found in csv."



    for row_idx, row in enumerate(read_distance_csv):

        for col_idx, column in enumerate(row):



                if col_idx < len(addresses):

                     address_1 = addresses[row_idx]
                     address_2 = addresses[col_idx]

                     return print(f"Distance between {address_1} and {address_2}: {column} miles")

'''