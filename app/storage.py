import yaml


def load():
    try:
        f = open('avti.yaml', 'r')
    except FileNotFoundError:
        return []

    res = yaml.load(f)
    f.close()
    return res['avti'] if (res is not None and 'avti' in res) else []


def save(avti):
    f = open('avti.yaml', 'w')

    f.write(yaml.dump({'avti': avti}))
    f.close()
