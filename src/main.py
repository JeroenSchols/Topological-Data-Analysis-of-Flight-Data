from src.Filters import *
from src.Utils import *
from ripser import ripser
from persim import plot_diagrams
import pandas as pd
import datetime
import tadasets
from scipy.spatial.distance import cdist


input_files = ["Dataset/" + str(y) + "-" + str(m+1).zfill(2) + ".csv" for m in range(1) for y in [2019]]
frames = [pd.read_csv(file, usecols=["FlightDate", "DepTime", "ArrTime", "OriginAirportID", "DestAirportID"]) for file in input_files]
flights = pd.concat(frames, ignore_index=True)

airports = pd.read_csv("Dataset/airports.csv", usecols=["AIRPORT_ID", "AIRPORT", "LATITUDE", "LONGITUDE"]).drop_duplicates("AIRPORT_ID").set_index("AIRPORT_ID", drop=False)

flights = day_filter(flights, datetime.datetime(2019, 1, 1), datetime.datetime(2019, 1, 10))

flights = merge_flights(flights)

IDtoIndex = list(set(flights["OriginAirportID"].tolist()).union(flights["DestAirportID"].tolist()))
IDtoIndex.sort()
IDtoIndex = {val: key for key, val in enumerate(IDtoIndex)}

dist_mat = distance_matrix(flights, IDtoIndex)
thresh = dist_mat.max()
dist_mat = (thresh - dist_mat)

IDtoCoordinates = pd.DataFrame.from_dict(IDtoIndex, orient='index').reset_index(drop=False).merge(airports, left_on='index', right_index=True)[['LONGITUDE', 'LATITUDE']]
coordinates = IDtoCoordinates.to_numpy()

result = ripser(dist_mat, distance_matrix=True, do_cocycles=True, thresh=thresh-0.00001)

cocycles = result['cocycles']

diagrams = result['dgms']


dgm1 = diagrams[1]
idx = np.argmax(dgm1[:, 1] - dgm1[:, 0])
cocycle = cocycles[1][idx]
thresh = dgm1[idx, 1]-0.00001 #Project cocycle onto edges less than or equal to death time
plotCocycle2D(dist_mat, coordinates, cocycle, thresh)
plt.title("1-Form Thresh=%g"%thresh)
plt.show()