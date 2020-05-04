import pandas as pd


# Filter flights based on start and end date
def day_filter(flight, start, end):
    flight['FlightDate'] = pd.to_datetime(flight['FlightDate'])
    print(flight.shape)
    filtered_flight = flight.query('@start <= FlightDate & FlightDate <= @end')
    print(filtered_flight.shape)
    return filtered_flight


def time_filter(flight, start, end):
    print(flight.shape)
    #Do lots of stuff to get time format to be usable for DepTime
    flight['DepTime'] = flight['DepTime'].astype(str).replace('\.0', '', regex=True)
    flight = flight.query('DepTime!="nan"')
    flight['DepTime'].replace({"2400": "0000"}, inplace=True)
    flight['DepTime'] = flight['DepTime'].str.zfill(4)
    flight['DepTime'] = flight['DepTime'].map(lambda a: a[:2] + ":" + a[2:])
    flight['DepTime'] = pd.to_datetime(flight['DepTime'], format = '%H:%M')

    #Same for ArrTime
    flight['ArrTime'] = flight['ArrTime'].astype(str).replace('\.0', '', regex=True)
    flight = flight.query('ArrTime!="nan"')
    flight['ArrTime'].replace({"2400": "0000"}, inplace=True)
    flight['ArrTime'] = flight['ArrTime'].str.zfill(4)
    flight['ArrTime'] = flight['ArrTime'].map(lambda a: a[:2] + ":" + a[2:])
    flight['ArrTime'] = pd.to_datetime(flight['ArrTime'], format = '%H:%M')

    filtered_flight = flight.query('(@start <= ArrTime & ArrTime <= @end) | (@start <= DepTime & DepTime <= @end)')
    print(filtered_flight.shape)
    return filtered_flight

