
def merge(old_cars, new_cars):
    added = []
    merged = []
    for new in new_cars:

        is_added = next((old for old in old_cars if old['id'] == new['id']), None) is not None

        if is_added:
            old_cars.pop(0)
        else:
            added.append(new)
        merged.append(new)

    merged = merged + old_cars
    return merged, added
