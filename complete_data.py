import csv
import random
from typing import List, Dict, Any

d = {
    (5, 4.5): "Excellent",
    (4, 3.5): "Very good",
    (3, 2.5): "Average",
    (2, 1.5): "Poor",
    (1, 0.5): "Terrible",
    (0, 0): "Bad"
}


# Get value to complete the gap
def get_value(value: Any) -> Any:
    for (upper, lower), exp in d.items():
        if isinstance(value, str):
            if value == exp:
                return random.choice([lower, upper])
        elif isinstance(value, float):
            if lower <= value <= upper:
                return exp
    return value


# Load data from .csv
def load_data(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]

        for row in data:
            if row['hotel_rating'] != "":
                row['hotel_rating'] = float(row['hotel_rating'])
            else:
                row['hotel_rating'] = None

            if row['hotel_experience'] == "":
                row['hotel_experience'] = None

            if row['hotel_rating'] is None and row['hotel_experience'] is None:
                row['hotel_rating'], row['hotel_experience'] = 0.0, "Bad"
            elif row['hotel_rating'] is None:
                row['hotel_rating'] = get_value(row['hotel_experience'])
            elif row['hotel_experience'] is None:
                row['hotel_experience'] = get_value(row['hotel_rating'])

            if row['price'] == "":
                row['price'] = 300
            else:
                row['price'] = float(row['price'])

            if row['amenities']:
                amenities_list = row['amenities'].strip("[]").split(", ")
                row['amenities'] = {amenity.strip("'") for amenity in amenities_list}
            else:
                row['amenities'] = set()

            if row['location'] and row["location"] != "('nil', 'nil')":
                location_str = row['location'].strip("()")
                lat_str, lon_str = location_str.split(", ")
                row['location'] = (float(lat_str), float(lon_str))
            else:
                row['location'] = (0.0, 0.0)

    return data


def write_data(file_path: str, data: List[Dict[str, Any]]):
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        fieldnames = ['id', 'hotel_name', 'hotel_rating', 'hotel_experience', 'amenities',
                      'address', 'country', 'locality', 'location', 'price', '']
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writeheader()
        for row in data:
            # Convert amenities back to string
            row['amenities'] = str(list(row['amenities']))
            # Convert location back to string
            row['location'] = f"({row['location'][0]}, {row['location'][1]})"
            writer.writerow(row)


file_path = 'hotel_info_dedup.csv'

hotels = load_data(file_path)
write_data(file_path, hotels)
