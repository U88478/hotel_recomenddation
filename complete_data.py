import csv
import random


r = csv.reader(open('hotel_info_dedup.csv'))
lines = list(r)

d = {(5, 4.5): "Excellent", (4, 3.5): "Very good", (3, 2.5): "Average", (2, 1.5): "Poor", (1, 0.5): "Terrible",
     (0, 0): "Bad"}


def get_value(v):
    for (l, u), op in d.items():
        if isinstance(v, str):
            if v == op:
                return random.choice([l, u])
        elif isinstance(v, float):
            if u < v < l:
                return op


for line in lines[1:]:
    if line[2] != "":
        line[2] = float(line[2])

    if line[2] == "" and line[3] == "":
        line[2], line[3] = 0.0, "Bad"
    elif line[2] == "":
        line[2] = get_value(line[3])
    elif line[3] == "":
        line[3] = get_value(line[2])

    if line[9] == "":
        line[9] = 300

with open('hotel_info_dedup.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerows(lines)
