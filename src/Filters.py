import pandas as pd


# Filter flights based on start and end date
def day_filter(flight, start, end):
    flight['FlightDate'] = pd.to_datetime(flight['FlightDate'])
    print(flight.shape)
    filtered_flight = flight.query('@start <= FlightDate & FlightDate <= @end')
    print(filtered_flight.shape)
    return filtered_flight


def time_filter(flight, start, end, inverse):
    print(flight.shape)
    # Do lots of stuff to get time format to be usable for DepTime
    flight['DepTime'] = flight['DepTime'].astype(
        str).replace('\.0', '', regex=True)
    flight = flight.query('DepTime!="nan"')
    flight['DepTime'].replace({"2400": "0000"}, inplace=True)
    flight['DepTime'] = flight['DepTime'].str.zfill(4)
    flight['DepTime'] = flight['DepTime'].map(lambda a: a[:2] + ":" + a[2:])
    flight['DepTime'] = pd.to_datetime(flight['DepTime'], format='%H:%M')

    # Same for ArrTime
    flight['ArrTime'] = flight['ArrTime'].astype(
        str).replace('\.0', '', regex=True)
    flight = flight.query('ArrTime!="nan"')
    flight['ArrTime'].replace({"2400": "0000"}, inplace=True)
    flight['ArrTime'] = flight['ArrTime'].str.zfill(4)
    flight['ArrTime'] = flight['ArrTime'].map(lambda a: a[:2] + ":" + a[2:])
    flight['ArrTime'] = pd.to_datetime(flight['ArrTime'], format='%H:%M')

    if inverse:
        filtered_flight = flight.query(
            '(DepTime < @start | DepTime > @end)')
    else:
        filtered_flight = flight.query(
            '(@start <= DepTime & DepTime <= @end)')
    print(filtered_flight.shape)
    return filtered_flight


# Filter flights based on airport
def airport_filter(flights, ids):
    print(flights.shape)
    filtered_flights = flights.query(
        'OriginAirportID in @ids | DestAirportID in @ids')
    print(filtered_flights.shape)
    return filtered_flights


# Calculate dictionary of frequency of an airportID occuring
def frame_to_frequency(flight, key):
    result = {}
    temp = flight.groupby(key).count()
    for key, value in temp.to_dict("index").items():
        result[key] = max(value.values())
    return result


# calculate summation of frequencies
def sum_frequencies(freq1, freq2):
    res = {}
    for key, value in freq1.items():
        if key in res:
            res[key] += value
        else:
            res[key] = value

    for key, value in freq2.items():
        if key in res:
            res[key] += value
        else:
            res[key] = value
    return res


# Filter all flights with airports visited less than provided frequency
def frequency_filter(flights_frequencies, min_frequency):
    filter_list = {}
    for key, value in flights_frequencies.items():
        if value >= min_frequency:
            filter_list[key] = value
    return filter_list
