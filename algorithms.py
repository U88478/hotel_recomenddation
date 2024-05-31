import time
from typing import List, Dict, Any


def insertion_sort(hotels: List[Dict[str, Any]], key: str) -> Dict[str, Any]:
    start_time = time.time()
    for i in range(1, len(hotels)):
        current = hotels[i]
        j = i - 1
        while j >= 0 and hotels[j][key] > current[key]:
            hotels[j + 1] = hotels[j]
            j -= 1
        hotels[j + 1] = current
    end_time = time.time()
    return {
        'sorted_hotels': hotels[-100:],
        'time': end_time - start_time
    }


def selection_sort(hotels: List[Dict[str, Any]], key: str) -> Dict[str, Any]:
    start_time = time.time()
    for i in range(len(hotels)):
        min_idx = i
        for j in range(i + 1, len(hotels)):
            if hotels[j][key] < hotels[min_idx][key]:
                min_idx = j
        hotels[i], hotels[min_idx] = hotels[min_idx], hotels[i]
    end_time = time.time()
    return {
        'sorted_hotels': hotels[-100:],
        'time': end_time - start_time
    }


def bubble_sort(hotels: List[Dict[str, Any]], key: str) -> Dict[str, Any]:
    start_time = time.time()
    n = len(hotels)
    for i in range(n):
        for j in range(0, n - i - 1):
            if hotels[j][key] > hotels[j + 1][key]:
                hotels[j], hotels[j + 1] = hotels[j + 1], hotels[j]
    end_time = time.time()
    return {
        'sorted_hotels': hotels[-100:],
        'time': end_time - start_time
    }
