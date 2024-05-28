import csv

# ['id', 'hotel_name', 'hotel_rating', 'hotel_experience', 'amenities', 'address', 'country', 'locality', 'location', 'price', '', '', '']

r = csv.reader(open('hotel_info_dedup.csv'))
lines = list(r)

li = set()

for line in lines[1:3]:
    li = set(line[4].strip("[]").split(", "))
    li = [x.strip("'") for x in li]
print("\n".join([x for x in li]))
