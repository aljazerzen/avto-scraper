import yaml


def get_list(storage, key):
    return storage[key] if (storage is not None and key in storage) else []


def load():
    try:
        f = open('storage.yaml', 'r')
    except FileNotFoundError:
        return [], []

    res = yaml.load(f)
    f.close()
    return get_list(res, 'all'), get_list(res, 'to_send')


def save(all_cars, to_send):
    f = open('storage.yaml', 'w')

    f.write(yaml.dump({
        'all': all_cars,
        'to_send': to_send
    }))
    f.close()
