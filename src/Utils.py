import numpy as np
import matplotlib.pyplot as plt


def merge_flights(flights):
    swap = flights["OriginAirportID"] > flights["DestAirportID"]
    flights.loc[swap, ["OriginAirportID", "DestAirportID"]] = flights.loc[swap, ["DestAirportID", "OriginAirportID"]].values
    flights = flights.groupby(["OriginAirportID", "DestAirportID"], as_index=False).size().reset_index().rename(columns={0:'count'})
    return flights


# compute distance matrix of pandas array based on a given mapping from id's to integers
def distance_matrix(flights, IDtoIndex):
    # initialize result with all zeroes
    res = np.zeros((len(IDtoIndex), len(IDtoIndex)))

    # generate matrix
    temp = flights.to_dict("index")
    for key, value in temp.items():
        res[IDtoIndex[value["OriginAirportID"]]][IDtoIndex[value["DestAirportID"]]] = value["count"]
        res[IDtoIndex[value["DestAirportID"]]][IDtoIndex[value["OriginAirportID"]]] = value["count"]
    # Return results
    return res

def drawLineColored(X, C):
    for i in range(X.shape[0]-1):
        plt.plot(X[i:i+2, 0], X[i:i+2, 1], c=C[i, :], lineWidth = 3)

def plotCocycle2D(D, X, cocycle, thresh):
    """
    Given a 2D point cloud X, display a cocycle projected
    onto edges under a given threshold "thresh"
    """
    #Plot all edges under the threshold
    N = X.shape[0]
    t = np.linspace(0, 1, 10)
    c = plt.get_cmap('Greys')
    C = c(np.array(np.round(np.linspace(0, 255, len(t))), dtype=np.int32))
    C = C[:, 0:3]

    for i in range(N):
        for j in range(N):
            if D[i, j] <= thresh:
                Y = np.zeros((len(t), 2))
                Y[:, 0] = X[i, 0] + t*(X[j, 0] - X[i, 0])
                Y[:, 1] = X[i, 1] + t*(X[j, 1] - X[i, 1])
                drawLineColored(Y, C)
    #Plot cocycle projected to edges under the chosen threshold
    for k in range(cocycle.shape[0]):
        [i, j, val] = cocycle[k, :]
        if D[i, j] <= thresh:
            [i, j] = [min(i, j), max(i, j)]
            a = 0.5*(X[i, :] + X[j, :])
            plt.text(a[0], a[1], '%g'%val, color='b')
    #Plot vertex labels
    for i in range(N):
        plt.text(X[i, 0], X[i, 1], '%i'%i, color='r')
    plt.axis('equal')
