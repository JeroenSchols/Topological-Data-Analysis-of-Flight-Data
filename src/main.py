from src.MapVisualizer import MapVisualizer
import pandas as pd
import numpy as np

flights = pd.read_csv("Dataset/2019-01.csv", usecols=["FlightDate", "DepTime", "OriginAirportID", "DestAirportID"])
airports = pd.read_csv("Dataset/airports.csv", usecols=["AIRPORT_ID", "AIRPORT", "LATITUDE", "LONGITUDE"]).drop_duplicates("AIRPORT_ID").set_index("AIRPORT_ID", drop=False)

mv = MapVisualizer()

for i, flight in flights.iterrows():
    source = airports.loc[flight["OriginAirportID"]]
    target = airports.loc[flight["DestAirportID"]]
    mv.add_vertex(source, 0)
    mv.add_vertex(target, 1)
    mv.add_edge(source, target, np.random.choice(range(256)))
    if i % 1000 == 0:
        print(i, len(flights))

mv.open_display()