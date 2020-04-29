import csv
from src.Graph_Based_Visualiser import GraphBasedVisualiser

coordinates = {}
with open('../Dataset/airports.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for line in reader:
        coordinates[line["AIRPORT_ID"]] = line["LATITUDE"] + "," + line["LONGITUDE"]

print(coordinates)

visualiser = GraphBasedVisualiser()
visualiser.addNode('EIN', 51.458369, 5.392055)  # Eindhoven Airport
visualiser.addNode('AMS', 52.310538, 4.768274)  # Amsterdam Airport Schiphol
visualiser.addNode('GRQ', 53.121666, 6.583331)  # Groningen Airport Eelde
visualiser.addNode('LEY', 52.455237, 5.520364)  # Lelystad Airport
visualiser.addNode('MST', 50.909496, 5.772830)  # Maastricht Aachen Airport
visualiser.addNode('RTM', 51.955508, 4.439883)  # Rotterdam The Hague Airport
visualiser.addEdge('EIN', 'AMS', 5)
visualiser.addEdge('GRQ', 'AMS', 10)
visualiser.addEdge('LEY', 'AMS', 15)
visualiser.addEdge('MST', 'AMS', 20)
visualiser.addEdge('RTM', 'AMS', 25)
visualiser.showGraph()
