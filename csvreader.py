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

with open ('WGUPS addressCSV.csv') as csvfile:
    read_dist_csv = csv.reader(csvfile, delimiter=',')

    for row, row_idx in enumerate(read_dist_csv):
         addresses.append(row_idx[1])

print(addresses)
with open('WGUPS distanceCSV.csv') as csvfile:
    read_distance_csv = csv.reader(csvfile, delimiter=',')



    for row_idx, row in enumerate(read_distance_csv):

        for col_idx, column in enumerate(row):



                if col_idx < len(addresses):

                     address_1 = addresses[row_idx]
                     address_2 = addresses[col_idx]

                     print(f"Distance between {address_1} and {address_2}: {column} miles")

