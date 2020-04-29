import csv

coordinates = {}
with open('../Dataset/airports.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for line in reader:
        coordinates[line["AIRPORT_ID"]] = [line["LATITUDE"], line["LONGITUDE"]]

print(coordinates)