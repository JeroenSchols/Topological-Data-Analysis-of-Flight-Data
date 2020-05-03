import pandas as pd


# Filter flights based on start and end date
def time_filter(flight, start, end):
    flight['FlightDate'] = pd.to_datetime(flight['FlightDate'])
    print(flight.shape)
    filtered_flight = flight.query('@start <= FlightDate & FlightDate <= @end')
    print(filtered_flight.shape)
    return filtered_flight
