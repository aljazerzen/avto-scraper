import yaml


def load():
    try:
        f = open('config.yaml', 'r')
    except FileNotFoundError:
        return {}

    try:
        return yaml.load(f)
    finally:
        f.close()
