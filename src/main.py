from src.MapVisualizer import MapVisualizer
from src.Graph_Based_Visualiser import GraphBasedVisualiser
from src.Filters import *
import pandas as pd
import numpy as np
import datetime

flights = pd.read_csv("Dataset/2019-01.csv", usecols=[
                      "FlightDate", "DepTime", "ArrTime", "OriginAirportID", "DestAirportID"])
airports = pd.read_csv("Dataset/airports.csv", usecols=["AIRPORT_ID", "AIRPORT", "LATITUDE",
                                                           "LONGITUDE"]).drop_duplicates("AIRPORT_ID").set_index("AIRPORT_ID", drop=False)

mv = MapVisualizer()
gv = GraphBasedVisualiser()

flights = day_filter(flights, datetime.datetime(
    2019, 1, 1), datetime.datetime(2019, 1, 1))
startTime = datetime.datetime(1900, 1, 1)
flights = time_filter(flights, startTime.replace(
    hour=10, minute=00), startTime.replace(hour=12, minute=00))

ids = [14771, 12892]
flights = airport_filter(flights, ids)


flights = frame_to_frequency(flights, ["OriginAirportID", "DestAirportID"])
flights = frequency_filter(flights, 3)

for (s, t) in flights:
    source = airports.loc[s]
    target = airports.loc[t]

    gv.add_vertex(source, flights[(s, t)])
    gv.add_vertex(target, flights[(s, t)])
    gv.add_edge(source, target, flights[(s, t)])
    # if i > 10000:
    #     break

gv.open_display()
mv.open_display()