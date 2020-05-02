from src.MapVisualizer import MapVisualizer
import pandas as pd
import numpy as np

flights = pd.read_csv("../Dataset/2019-01.csv", usecols=["FlightDate", "DepTime", "OriginAirportID", "DestAirportID"])
airports = pd.read_csv("../Dataset/airports.csv", usecols=["AIRPORT_ID", "AIRPORT", "LATITUDE", "LONGITUDE"], index_col=["AIRPORT_ID"])

mv = MapVisualizer()

for i, airport in airports.iterrows():
    # currently choses arbitrary colors
    mv.add_vertex(airport, np.random.choice(range(256)))

print(isinstance(pd.DataFrame,pd.Series))
print(isinstance(pd.Series,pd.DataFrame))

for i, flight in flights.iterrows():
    # @TODO should have source and target airports of flights

    #get check if airpot id is contained multiple times
    #if so, get the first aiport that belongs to the given id
    #else get the unique airport related to the id
    if isinstance(airports.loc[flight["OriginAirportID"]], pd.DataFrame):
        for j, airport in airports.loc[flight["OriginAirportID"]].iterrows():
            source = airport
            break
    else:
        source = airports.loc[flight["OriginAirportID"]]

    if isinstance(airports.loc[flight["DestAirportID"]], pd.DataFrame):
        for j, airport in airports.loc[flight["DestAirportID"]].iterrows():
            target = airport
            break
    else:
        target = airports.loc[flight["DestAirportID"]]

    if i > 50:
        break
    mv.add_edge(source, target, np.random.choice(range(256)))

mv.open_display()