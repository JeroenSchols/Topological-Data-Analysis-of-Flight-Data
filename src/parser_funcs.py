import numpy as np
import pandas as pd
import calendar
import copy
import re
from datetime import date



month_to_num = {k: v for v, k in enumerate(calendar.month_name)}
weekdays = calendar.day_name[:5]

def results_day_night_to_latex(results, output_name):
    sum_clust = {}
    for month, times in results.items():
        max = np.max([np.max(x) for _, x in times.items()])
        summed = {}
        if (max == -1):
            continue
        for time, clusts in times.items():
            day_sum = [0] * (max + 1)
            for clust in clusts:
                day_sum[clust] += 1
            summed[time] = day_sum
        sum_clust[month] = pd.DataFrame.from_dict(summed)

    final = None
    with open(f"Clusters/{output_name}.tex", "w") as f:
        for month, times in sum_clust.items():
            if len(times.index) == 0:
                continue
            cluster_amount = times.index[-1]
            tups = []
            day_night = [0] * (cluster_amount + 1)

            for key, val in times.iteritems():
                temp = [x for x in val]
                tups.append(str(temp))

            tups = tups
            columns = list(times.columns)

            if final is None:
                final = pd.DataFrame(np.array(tups).reshape((1, 2)), columns=columns,
                                     index=[calendar.month_name[month]])
            else:
                final = final.append(
                    pd.DataFrame(np.array(tups).reshape((1, 2)), columns=columns, index=[calendar.month_name[month]]))
        f.write(final.to_latex())




def results_to_latex(results, output_name):
    """
    takes a  map from file name to pandas dataframe and computes final concatonated list
    """

    results_sum_clust = {}
    for file, result in results.items():
        max = np.max([np.max(x) for _, x in result.items()])
        if (max == -1):
            continue
        day_sum = {}
        for day, clusters in result.items():
            day_sum[day] = [0] * (max + 1)
            for cluster in clusters:

                day_sum[day][cluster] += 1
        results_sum_clust[file] = pd.DataFrame.from_dict(day_sum)

    final = None
    summed = None
    with open(f"Clusters/{output_name}.tex", "w") as f:
        for month, results in results_sum_clust.items():
            if len(results.index) == 0:
                continue
            cluster_amount = results.index[-1]
            tups = []
            weekday = [0]*(cluster_amount+1)
            weekend = [0]*(cluster_amount+1)

            for key, val in results.iteritems():
                temp = [x for x in val]
                tups.append(str(temp))
                if key in weekdays:
                    weekday = [x + y for x, y in zip(weekday, temp)]
                else:
                    weekend = [x + y for x, y in zip(weekend, temp)]

            tups = tups
            columns = list(results.columns)

            if final is None:
                final = pd.DataFrame(np.array(tups).reshape((1,7)), columns = columns, index = [calendar.month_name[month]])
                summed = pd.DataFrame(np.array([str(weekday),str(weekend)]).reshape((1,2)), columns = ["Weekdays", "Weekends"], index = [calendar.month_name[month]])
            else:
                final = final.append(pd.DataFrame(np.array(tups).reshape((1,7)), columns = columns, index = [calendar.month_name[month]]))
                summed = summed.append(pd.DataFrame(np.array([str(weekday), str(weekend)]).reshape((1, 2)),columns=["Weekdays", "Weekends"], index=[calendar.month_name[month]]))
        f.write(final.to_latex())
        f.write(summed.to_latex())