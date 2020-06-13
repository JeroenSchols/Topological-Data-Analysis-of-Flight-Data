import numpy as np
import pandas as pd
import calendar
import copy
import re
from datetime import date
from src.parser_funcs import *

zero_persistence_file = "Clusters/Zero persistence/res.txt"
one_persistence_file = "Clusters/One persistence/res.txt"
files = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
files_appended = ["Zero One persistence/"+file+".txt" for file in files]
file_to_month = {file: month for num, (month, file) in enumerate(zip(files, files_appended))}
month_to_num = {k: v for v, k in enumerate(calendar.month_name)}
print(month_to_num)
default = {day:[] for day in calendar.day_name}
results = {}

weekdays = calendar.day_name[:5]
print(weekdays)

# parse zero one data
for file in files_appended:
    month = month_to_num[file_to_month[file]]
    with open(f"Clusters/{file}") as f:
        result = copy.deepcopy(default)
        current = []
        for line in f:
            split = re.split(", |=|\n",line)
            current.append([int(split[1]),int(split[2])])
        for data in current:
            day = date(2019, month, data[0]).weekday()
            day = calendar.day_name[int(day)]
            result[day].append(data[1])
        results[month] = result

# results_to_latex(results, "testing")

results2 = {}
result = copy.deepcopy(default)
with open(zero_persistence_file) as file:
    prev_month = 0
    for line in file:
        split = re.split(",|=|\n",line)
        month = int(split[1])
        day = int(split[3])
        clust = int(split[4])
        if month == prev_month:
            day = calendar.day_name[date(2019, month, day).weekday()]
            result[day].append(clust)
            results[month] = result
            prev_month = month
        else:
            result = copy.deepcopy(default)
            day = calendar.day_name[date(2019, month, day).weekday()]
            result[day].append(clust)
            results2[month] = result
            prev_month = month

results_to_latex(results, "zero_tabs")

results3 = {}
result = copy.deepcopy(default)
with open(one_persistence_file) as file:
    prev_month = 0
    for line in file:
        if line == "\n":
            continue

        if "Month" in line:
            line = file.__next__()
            month = int(line)
            result = copy.deepcopy(default)
            continue

        split = re.split(",|=|\n",line)
        day = int(split[1])
        clust = int(split[2])
        if month == prev_month:
            day = calendar.day_name[date(2019, month, day).weekday()]
            result[day].append(clust)
            results[month] = result
            prev_month = month
        else:
            result = copy.deepcopy(default)
            day = calendar.day_name[date(2019, month, day).weekday()]
            result[day].append(clust)
            results3[month] = result
            prev_month = month




print(results)
results_to_latex(results, "one_tabs")




# print(results_sum_clust[files[0]].sum().tolist())
