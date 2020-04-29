import csv
from src.Visualizer import Visualizer

coordinates = {}
with open('../Dataset/airports.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for line in reader:
        coordinates[line["AIRPORT_ID"]] = [line["LATITUDE"], line["LONGITUDE"]]

# test = Visualizer(["2019-01.csv"])
# print(test.data)