from src.MapVisualizer import MapVisualizer
import pandas as pd
import numpy as np
import datetime

flights = pd.read_csv("../Dataset/2019-01.csv", usecols=["FlightDate", "DepTime", "OriginAirportID", "DestAirportID"])
airports = pd.read_csv("../Dataset/airports.csv", usecols=["AIRPORT_ID", "AIRPORT", "LATITUDE", "LONGITUDE"], index_col=["AIRPORT_ID"])

mv = MapVisualizer()

flights = time_filter(flights, datetime.datetime(2019, 1, 1), datetime.datetime(2019, 1, 10))

for i, airport in airports.iterrows():
    # currently choses arbitrary colors
    mv.add_vertex(airport, np.random.choice(range(256)))

print(isinstance(pd.DataFrame,pd.Series))
print(isinstance(pd.Series,pd.DataFrame))

for i, flight in flights.iterrows():
    source = airports.loc[flight["OriginAirportID"]]
    target = airports.loc[flight["DestAirportID"]]
    mv.add_vertex(source, 0)
    mv.add_vertex(target, 1)
    mv.add_edge(source, target, np.random.choice(range(256)))
    if i > 10000:
        break

mv.open_display()