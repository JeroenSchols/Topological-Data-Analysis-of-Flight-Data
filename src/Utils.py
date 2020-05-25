import numpy as np


def merge_flights(flights):
    swap = flights["OriginAirportID"] > flights["DestAirportID"]
    flights.loc[swap, ["OriginAirportID", "DestAirportID"]] = flights.loc[swap, ["DestAirportID", "OriginAirportID"]].values
    flights = flights.groupby(["OriginAirportID", "DestAirportID"], as_index=False).size().reset_index().rename(columns={0:'count'})
    return flights


# compute distance matrix of pandas array based on a given mapping from id's to integers
def distance_matrix(flights, IDtoIndex):
    # initialize result with all zeroes
    res = np.zeros((len(IDtoIndex), len(IDtoIndex)))

    # generate matrix
    temp = flights.to_dict("index")
    for key, value in temp.items():
        res[IDtoIndex[value["OriginAirportID"]]][IDtoIndex[value["DestAirportID"]]] = value["count"]
        res[IDtoIndex[value["DestAirportID"]]][IDtoIndex[value["OriginAirportID"]]] = value["count"]
    # Return results
    return res

