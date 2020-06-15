#from src.MapVisualizer import MapVisualizer
#from src.Graph_Based_Visualiser import GraphBasedVisualiser
from src.Filters import *
from src.Utils import *
from ripser import ripser
from persim import plot_diagrams
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
import persim
from sklearn.cluster import AffinityPropagation

use_zero_persistence = False
use_first_persistence = True

day_months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

for month in range(1, 13):
    print("Month")
    print(month)

    # load and parse input files
    input_files = ["Dataset/" + str(y) + "-" + str(m+1).zfill(2) + ".csv" for m in range(month-1, month) for y in [2019]]
    frames = [pd.read_csv(file, usecols=["FlightDate", "DepTime", "ArrTime", "OriginAirportID", "DestAirportID"]) for file in input_files]
    flights = pd.concat(frames, ignore_index=True)
    airports = pd.read_csv("Dataset/airports.csv", usecols=["AIRPORT_ID", "AIRPORT", "LATITUDE", "LONGITUDE"])\
        .drop_duplicates("AIRPORT_ID").set_index("AIRPORT_ID", drop=False)
    IDtoIndex = list(set(flights["OriginAirportID"].tolist()).union(flights["DestAirportID"].tolist()))
    IDtoIndex.sort()
    IDtoIndex = {val: key for key, val in enumerate(IDtoIndex)}

    group_data = []
    idx_to_name = []



    # filter dataset
    for day in range(1, day_months[month] + 1):
        idx_to_name.append("month = " + str(month) + "day = " + str(day))
        subset_flights = day_filter(flights, datetime.datetime(2019, month, day), datetime.datetime(2019, month, day))
        group_data.append(subset_flights)

        # # Needed to set time for time_filter
        # startTime = datetime.datetime(1900, 1, 1)

        # subset_flights = day_filter(flights, datetime.datetime(2019, 2, day), datetime.datetime(2019, 2, day))
        # day_flights = time_filter(subset_flights, startTime.replace(hour=6, minute=00), startTime.replace(hour=18, minute=00), False)
        # group_data.append(day_flights)
        #
        # idx_to_name.append("night = " + str(day))
        # night_flights = time_filter(subset_flights, startTime.replace(hour=6, minute=00), startTime.replace(hour=18, minute=00), True)
        # group_data.append(night_flights)

    # transform data from single flights to (origin, destination, count)
    group_data = [merge_flights(subset_flights) for subset_flights in group_data]

    # compute distance matrices
    distance_matrices = []
    for subset_flights in group_data:
        dist_matrix = distance_matrix(subset_flights, IDtoIndex)
        dist_matrix = dist_matrix.max() - dist_matrix
        dist_matrix = dist_matrix - (np.identity(len(dist_matrix))*np.max(dist_matrix))
        distance_matrices.append(dist_matrix)

    # compute persistence diagrams
    print("computing persistence diagrams")
    persist_diagrams = []
    for dist_matrix in distance_matrices:
        dgms = None
        if use_zero_persistence & use_first_persistence:
            dgms = ripser(dist_matrix, distance_matrix=True)['dgms']
        elif use_zero_persistence:
            dgms = ripser(dist_matrix, distance_matrix=True)['dgms'][0]
        elif use_first_persistence:
            dgms = ripser(dist_matrix, distance_matrix=True)['dgms'][1]
        else:
            print("should use at least zero or first persistence metric")
            assert False
        persist_diagrams.append(dgms)

    print("computing bottleneck distance")
    bottleneck_distances = []
    for i, dist_matrix1 in enumerate(distance_matrices):
        print(i)
        distances = []
        for j, dist_matrix2 in enumerate(distance_matrices):
            if i > j:
                distances.append(bottleneck_distances[j][i])
            else:
                distance = persim.bottleneck(dist_matrix1, dist_matrix2)
                distances.append(distance)
        bottleneck_distances.append(distances)

    print("clustering")
    clustering = AffinityPropagation(affinity='precomputed').fit(bottleneck_distances)
    clustering = [(idx_to_name[idx], cluster) for idx, cluster in enumerate(clustering.labels_)]
    for name, cluster in clustering:
        print(name, ",", cluster)

    # # gnt.set_xlabel("lifetime")
    # # gnt.set_yticks(range(a*2))
    # # gnt.set_ylabel("H0")
    # for idx, bar in enumerate(dgms[0]):
    #     # print(f"idx {idx}  bar {bar}")
    #     gnt.broken_barh([(bar[0], bar[1]-bar[0])], (idx, 0.5))
    # # fig.set_figheight(300)
    # # fig.set_figwidth(20)
    # plt.savefig("H0.pdf")
    #
    # plt.rcdefaults()
    # fig, gnt = plt.subplots()
    #
    # for idx, bar in enumerate(dgms[1]):
    #     # print(f"idx {idx}  bar {bar}")
    #     gnt.broken_barh([(bar[0], bar[1]-bar[0])], (idx, 0.5), facecolors = ("tab:orange"))
    # plt.savefig("H1.pdf")
