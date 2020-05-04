import pandas as pd


# Filter flights based on start and end date
def time_filter(flights, start, end):
    flights['FlightDate'] = pd.to_datetime(flights['FlightDate'])
    print(flights.shape)
    filtered_flights = flights.query('@start <= FlightDate & FlightDate <= @end')
    print(filtered_flights.shape)
    return filtered_flights


# Filter flights based on airport
def airport_filter(flights, ids):
    print(flights.shape)
    filtered_flights = flights.query('OriginAirportID in @ids | DestAirportID in @ids')
    print(filtered_flights.shape)
    return filtered_flights

def frame_to_frequency(flight, key):
    result = {}
    temp = flight.groupby(key).count()
    for key, value in temp.to_dict("index").items():
        result[key] = max(value.values())
    return result
