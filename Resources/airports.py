#!env python3
import csv
# read in CSV file
filepath = './airports_utf.csv'
with open(filepath, 'r') as fh:
    reader = csv.reader(fh)
    data = list(reader)

for row in data:
  row.append(row[0])

with open('new_airports.csv', 'w') as fh:
    writer = csv.writer(fh)
    writer.writerows(data)
