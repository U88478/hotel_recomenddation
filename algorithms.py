import time
from typing import List, Dict, Any

review_map = {
    "Excellent": 5,
    "Very good": 4,
    "Average": 3,
    "Poor": 2,
    "Terrible": 1,
    "Bad": 0
}


def insertion_sort(hotels: List[Dict[str, Any]], key: str) -> Dict[str, Any]:
    start_time = time.time()
    for i in range(1, len(hotels)):
        current = hotels[i]
        j = i - 1
        while j >= 0 and (review_map[hotels[j][key]] < review_map[current[key]] if key == 'hotel_experience'
                else hotels[j][key] < current[key]):
            hotels[j + 1] = hotels[j]
            j -= 1
        hotels[j + 1] = current
    end_time = time.time()
    return {
        'sorted_hotels': hotels[:100],
        'time': end_time - start_time
    }


def selection_sort(hotels: List[Dict[str, Any]], key: str) -> Dict[str, Any]:
    start_time = time.time()
    for i in range(len(hotels)):
        max_idx = i
        for j in range(i + 1, len(hotels)):
            if (review_map[hotels[j][key]] > review_map[hotels[max_idx][key]] if key == 'hotel_experience'
                    else hotels[j][key] > hotels[max_idx][key]):
                max_idx = j
        hotels[i], hotels[max_idx] = hotels[max_idx], hotels[i]
    end_time = time.time()
    return {
        'sorted_hotels': hotels[:100],
        'time': end_time - start_time
    }


def bubble_sort(hotels: List[Dict[str, Any]], key: str) -> Dict[str, Any]:
    start_time = time.time()
    n = len(hotels)
    for i in range(n):
        for j in range(0, n - i - 1):
            if review_map[hotels[j][key]] < review_map[hotels[j + 1][key]] if key == 'hotel_experience' \
                    else hotels[j][key] < hotels[j + 1][key]:
                hotels[j], hotels[j + 1] = hotels[j + 1], hotels[j]
    end_time = time.time()
    return {
        'sorted_hotels': hotels[:100],
        'time': end_time - start_time
    }
