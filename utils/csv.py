from typing import List


def get_values_from_csv(csv) -> List:
    return csv.strip().split(', ')
