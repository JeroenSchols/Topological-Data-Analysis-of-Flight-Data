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

# load and parse input files
input_files = ["Dataset/" + str(y) + "-" + str(m+1).zfill(2) + ".csv" for m in range(0, 1) for y in [2019]]
frames = [pd.read_csv(file, usecols=["FlightDate", "DepTime", "ArrTime", "OriginAirportID", "DestAirportID"]) for file in input_files]
flights = pd.concat(frames, ignore_index=True)
airports = pd.read_csv("Dataset/airports.csv", usecols=["AIRPORT_ID", "AIRPORT", "LATITUDE", "LONGITUDE"])\
    .drop_duplicates("AIRPORT_ID").set_index("AIRPORT_ID", drop=False)
IDtoIndex = list(set(flights["OriginAirportID"].tolist()).union(flights["DestAirportID"].tolist()))
IDtoIndex.sort()
IDtoIndex = {val: key for key, val in enumerate(IDtoIndex)}

group_data = []
# filter dataset
for day in range(1, 32):
    name = "day = " + str(day)
    subset_flights = day_filter(flights, datetime.datetime(2019, 1, day), datetime.datetime(2019, 1, day))
    group_data.append((name, subset_flights))

# transform data from single flights to (origin, destination, count)
group_data = [(name, merge_flights(subset_flights)) for name, subset_flights in group_data]

# compute distance matrices
distance_matrices = []
for name, subset_flights in group_data:
    dist_matrix = distance_matrix(subset_flights, IDtoIndex)
    dist_matrix = dist_matrix.max() - dist_matrix
    dist_matrix = dist_matrix - (np.identity(len(dist_matrix))*np.max(dist_matrix))
    distance_matrices.append((name, dist_matrix))

# compute persistence diagrams
print("computing persistence diagrams")
persist_diagrams = []
for name, dist_matrix in distance_matrices:
    dgms = ripser(dist_matrix, distance_matrix=True)['dgms']
    persist_diagrams.append((name, dgms))

print("computing bottleneck distance")
bottleneck_distances = []
for name1, dist_matrix1 in distance_matrices:
    distances = []
    for name2, dist_matrix2 in distance_matrices:
        distance = persim.bottleneck(dist_matrix1, dist_matrix2)
        distances.append(distance)
    bottleneck_distances.append(distances)


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