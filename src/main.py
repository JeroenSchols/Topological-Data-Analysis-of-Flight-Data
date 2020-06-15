from src.MapVisualizer import MapVisualizer
from src.Graph_Based_Visualiser import GraphBasedVisualiser
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
import src.Visualizer
import src.MapVisualizer

use_zero_persistence = True
use_first_persistence = False

# load and parse input files
input_files = ["Dataset/" + str(y) + "-" + str(m+1).zfill(2) + ".csv" for m in range(1) for y in [2019]]
frames = [pd.read_csv(file, usecols=["FlightDate", "DepTime", "ArrTime", "OriginAirportID", "DestAirportID"]) for file in input_files]
flights = pd.concat(frames, ignore_index=True)
airports = pd.read_csv("Dataset/airports.csv", usecols=["AIRPORT_ID", "AIRPORT", "LATITUDE", "LONGITUDE"])\
    .drop_duplicates("AIRPORT_ID").set_index("AIRPORT_ID", drop=False)
IDtoIndex = list(set(flights["OriginAirportID"].tolist()).union(flights["DestAirportID"].tolist()))
IDtoIndex.sort()
IDtoIndex = {val: key for key, val in enumerate(IDtoIndex)}

mv = MapVisualizer()

flights = merge_flights(flights)
flights = flights[flights['count'] > 500]

a_col = {}
for i, airport in airports.iterrows():
    a_col[i] = np.random.choice(range(256))

for i, flight in flights.iterrows():
    source = airports.loc[flight["OriginAirportID"]]
    target = airports.loc[flight["DestAirportID"]]
    if source["LONGITUDE"] < -130 or target["LONGITUDE"] < -130 or source["LONGITUDE"] > -65 or target["LONGITUDE"] > -65 or source["LATITUDE"] < 25 or target["LATITUDE"] < 25:
        print(source["LONGITUDE"], source["LATITUDE"], source["AIRPORT"], target["LONGITUDE"], target["LATITUDE"], target["AIRPORT"])
        continue
    mv.add_vertex(source, a_col[flight["OriginAirportID"]])
    mv.add_vertex(target, a_col[flight["DestAirportID"]])
    mv.add_edge(source, target, a_col[flight["OriginAirportID"]])

mv.open_display()

#
# day_months = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
#
# for month in range(1, 13):
#
#     group_data = []
#     idx_to_name = []
#
#     # Needed to set time for time_filter
#     startTime = datetime.datetime(1900, 1, 1)
#
#     # filter dataset
#     for day in range(1, day_months[month] + 1):
#         idx_to_name.append("month = " + str(month) + "day = " + str(day))
#         subset_flights = day_filter(flights, datetime.datetime(2019, month, day), datetime.datetime(2019, month, day))
#         group_data.append(subset_flights)
#
#     # transform data from single flights to (origin, destination, count)
#     group_data = [merge_flights(subset_flights) for subset_flights in group_data]
#
#     # compute distance matrices
#     distance_matrices = []
#     for subset_flights in group_data:
#         dist_matrix = distance_matrix(subset_flights, IDtoIndex)
#         dist_matrix = dist_matrix.max() - dist_matrix
#         dist_matrix = dist_matrix - (np.identity(len(dist_matrix))*np.max(dist_matrix))
#         distance_matrices.append(dist_matrix)
#
#     # compute persistence diagrams
#     print("computing persistence diagrams")
#     persist_diagrams = []
#     for dist_matrix in distance_matrices:
#         dgms = None
#
#         print("tot", len(ripser(dist_matrix, distance_matrix=True)['dgms']))
#         print("0", len(ripser(dist_matrix, distance_matrix=True)['dgms'][0]))
#         print("1", len(ripser(dist_matrix, distance_matrix=True)['dgms'][1]))
#         if use_zero_persistence & use_first_persistence:
#             dgms = ripser(dist_matrix, distance_matrix=True)['dgms']
#         elif use_zero_persistence:
#             dgms = ripser(dist_matrix, distance_matrix=True)['dgms'][0]
#         elif use_first_persistence:
#             dgms = ripser(dist_matrix, distance_matrix=True)['dgms'][1]
#         else:
#             print("should use at least zero or first persistence metric")
#             assert False
#         persist_diagrams.append(dgms)
#
#     print("computing bottleneck distance")
#     bottleneck_distances = []
#     for i, dist_matrix1 in enumerate(distance_matrices):
#         distances = []
#         for j, dist_matrix2 in enumerate(distance_matrices):
#             if i > j:
#                 distances.append(bottleneck_distances[j][i])
#             else:
#                 distance = persim.bottleneck(dist_matrix1, dist_matrix2)
#                 distances.append(distance)
#         bottleneck_distances.append(distances)
#
#     print("clustering")
#     clustering = AffinityPropagation(affinity='precomputed').fit(bottleneck_distances)
#     clustering = [(idx_to_name[idx], cluster) for idx, cluster in enumerate(clustering.labels_)]
#     for name, cluster in clustering:
#         print(name, ",", cluster)
#
# # # gnt.set_xlabel("lifetime")
# # # gnt.set_yticks(range(a*2))
# # # gnt.set_ylabel("H0")
# # for idx, bar in enumerate(dgms[0]):
# #     # print(f"idx {idx}  bar {bar}")
# #     gnt.broken_barh([(bar[0], bar[1]-bar[0])], (idx, 0.5))
# # # fig.set_figheight(300)
# # # fig.set_figwidth(20)
# # plt.savefig("H0.pdf")
# #
# # plt.rcdefaults()
# # fig, gnt = plt.subplots()
# #
# # for idx, bar in enumerate(dgms[1]):
# #     # print(f"idx {idx}  bar {bar}")
# #     gnt.broken_barh([(bar[0], bar[1]-bar[0])], (idx, 0.5), facecolors = ("tab:orange"))
# # plt.savefig("H1.pdf")