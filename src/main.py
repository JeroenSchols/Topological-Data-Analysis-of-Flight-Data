#from src.MapVisualizer import MapVisualizer
from src.Graph_Based_Visualiser import GraphBasedVisualiser
from src.Filters import *
import pandas as pd
import numpy as np
import datetime

flights = pd.read_csv("Dataset/2019-01.csv", usecols=[
                      "FlightDate", "DepTime", "ArrTime", "OriginAirportID", "DestAirportID"])
airports = pd.read_csv("Dataset/airports.csv", usecols=["AIRPORT_ID", "AIRPORT", "LATITUDE",
                                                           "LONGITUDE"]).drop_duplicates("AIRPORT_ID").set_index("AIRPORT_ID", drop=False)

#mv = MapVisualizer()
gv = GraphBasedVisualiser()

flights = day_filter(flights, datetime.datetime(
    2019, 1, 1), datetime.datetime(2019, 1, 1))
startTime = datetime.datetime(1900, 1, 1)
flights = time_filter(flights, startTime.replace(
    hour=10, minute=00), startTime.replace(hour=12, minute=00))

ids = [14771, 12892]
flights = airport_filter(flights, ids)


flight_freq_origin = frame_to_frequency(flights, "OriginAirportID")
flight_freq_dest = frame_to_frequency(flights, "DestAirportID")
flight_freq_sum = sum_frequencies(flight_freq_origin, flight_freq_dest)


flights = frequency_filter(flights, flight_freq_sum, 50)


for i, flight in flights.iterrows():
    source = airports.loc[flight["OriginAirportID"]]
    target = airports.loc[flight["DestAirportID"]]
    freq_source = flight_freq_sum[flight["OriginAirportID"]]
    freq_target = flight_freq_sum[flight["DestAirportID"]]

    mv.add_vertex(source, freq_source)
    mv.add_vertex(target, freq_target)
    mv.add_edge(source, target, max(freq_source,freq_target))

    gv.add_vertex(source, freq_source)
    gv.add_vertex(target, freq_target)
    gv.add_edge(source, target, max(freq_source, freq_target))
    # if i > 10000:
    #     break

gv.open_display()
mv.open_display()