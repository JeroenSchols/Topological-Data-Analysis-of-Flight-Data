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


input_files = ["Dataset/" + str(y) + "-" + str(m+1).zfill(2) + ".csv" for m in range(11, 12) for y in [2019]]
frames = [pd.read_csv(file, usecols=["FlightDate", "DepTime", "ArrTime", "OriginAirportID", "DestAirportID"]) for file in input_files]
flights = pd.concat(frames, ignore_index=True)

airports = pd.read_csv("Dataset/airports.csv", usecols=["AIRPORT_ID", "AIRPORT", "LATITUDE", "LONGITUDE"])\
    .drop_duplicates("AIRPORT_ID").set_index("AIRPORT_ID", drop=False)

# mv = MapVisualizer()
# gv = GraphBasedVisualiser()

flights = day_filter(flights, datetime.datetime(2019, 12, 25), datetime.datetime(2019, 12, 26))

# startTime = datetime.datetime(1900, 1, 1)
# flights = time_filter(flights, startTime.replace(hour=6, minute=00), startTime.replace(hour=18, minute=00), True)
# ids = [14771, 12892]
# flights = airport_filter(flights, ids)

# flights = frame_to_frequency(flights, ["OriginAirportID", "DestAirportID"])
# flights = frequency_filter(flights, 3)

flights = merge_flights(flights)

# dist = distance_matrix(flights)
IDtoIndex = list(set(flights["OriginAirportID"].tolist()).union(flights["DestAirportID"].tolist()))
IDtoIndex.sort()
IDtoIndex = {val: key for key, val in enumerate(IDtoIndex)}
print(flights)

dist_mat = distance_matrix(flights, IDtoIndex)
print(dist_mat)
dist_mat = (dist_mat.max() - dist_mat)
dist_mat = dist_mat - (np.identity(len(dist_mat))*np.max(dist_mat))
print(dist_mat)
dgms = ripser(dist_mat, distance_matrix=True)['dgms']
plot_diagrams(dgms, show=True)
a = len(dgms[0])
print(a)
# print(dgms)

plt.rcdefaults()
fig, gnt = plt.subplots()

# gnt.set_xlabel("lifetime")
# gnt.set_yticks(range(a*2))
# gnt.set_ylabel("H0")
for idx, bar in enumerate(dgms[0]):
    # print(f"idx {idx}  bar {bar}")
    gnt.broken_barh([(bar[0], bar[1]-bar[0])], (idx, 0.5))
# fig.set_figheight(300)
# fig.set_figwidth(20)
plt.savefig("H0.pdf")

plt.rcdefaults()
fig, gnt = plt.subplots()

for idx, bar in enumerate(dgms[1]):
    # print(f"idx {idx}  bar {bar}")
    gnt.broken_barh([(bar[0], bar[1]-bar[0])], (idx, 0.5), facecolors = ("tab:orange"))
plt.savefig("H1.pdf")

# for (s, t) in flights:
#     source = airports.loc[s]
#     target = airports.loc[t]
#
#     gv.add_vertex(source, flights[(s, t)])
#     gv.add_vertex(target, flights[(s, t)])
#     gv.add_edge(source, target, flights[(s, t)])
#     # if i > 10000:
#     #     break
#
# gv.open_display()
# mv.open_display()