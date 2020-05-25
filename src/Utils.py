def merge_flights(flights):
    swap = flights["OriginAirportID"] > flights["DestAirportID"]
    flights.loc[swap, ["OriginAirportID", "DestAirportID"]] = flights.loc[swap, ["DestAirportID", "OriginAirportID"]].values
    flights = flights.groupby(["OriginAirportID", "DestAirportID"], as_index=False).size().reset_index().rename(columns={0:'count'})
    return flights