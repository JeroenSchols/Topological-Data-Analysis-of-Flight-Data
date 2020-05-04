import pandas as pd


# Filter flights based on start and end date
def time_filter(flights, start, end):
    flights['FlightDate'] = pd.to_datetime(flights['FlightDate'])
    print(flights.shape)
    filtered_flights = flights.query('@start <= FlightDate & FlightDate <= @end')
    print(filtered_flights.shape)
    return filtered_flights


# Filter flights based on airport
def airport_filter(flights, id):
    print(flights.shape)
    filtered_flights = flights.query('OriginAirportID == @id | DestAirportID == @id')
    print(filtered_flights.shape)
    return filtered_flights