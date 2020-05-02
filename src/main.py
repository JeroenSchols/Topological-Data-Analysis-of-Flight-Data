from src.MapVisualizer import MapVisualizer
import pandas as pd
import numpy as np

flights = pd.read_csv("../Dataset/2019-01.csv", usecols=["FlightDate", "DepTime", "OriginAirportID", "DestAirportID"])
airports = pd.read_csv("../Dataset/airports.csv", usecols=["AIRPORT_ID", "AIRPORT", "LATITUDE", "LONGITUDE"], index_col=["AIRPORT_ID"])

mv = MapVisualizer()

for i, airport in airports.iterrows():
    # currently choses arbitrary colors
    mv.add_vertex(airport, np.random.choice(range(256)))

for i, flight in flights.iterrows():
    # @TODO should have source and target airports of flights
    source = airports.sample()
    target = airports.sample()
    if i > 50:
        break
    mv.add_edge(source, target, np.random.choice(range(256)))

mv.open_display()