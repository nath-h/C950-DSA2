import csv

addresses = []
matrix=[]
with open('WGUPS Distance Table2.csv', mode='r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        matrix.append(row)


    addresses = [row[0].strip() for row in matrix[1:]]
print(addresses)


with open('WGUPS Distance Table2.csv', mode='r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        matrix.append(row)


for row_idx, row in enumerate(matrix):
    for col_idx, value in enumerate(row):
        print(f"Element at ({row_idx}, {col_idx}): {value}")