from app.config import FILTER

def filter_cars(cars):
    return [car for car in cars if
            (FILTER['max_price'] is None or (car['price'] is not None and car['price'] <= FILTER['max_price'])) and
            (FILTER['max_km'] is None or (car['km'] is not None and car['km'] <= FILTER['max_km']))
            ]


def filters_to_string():
    r = []
    for key, value in FILTER.items():
        r.append(str(key) + ": " + str(value))
    return ", ".join(r)
