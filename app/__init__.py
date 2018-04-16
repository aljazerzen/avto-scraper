from time import sleep, time
from app import config, storage, mail
from app.scrape import scrape
from app.service import merge, filter_cars


def app():
    last_send = 0

    while True:
        scraped = filter_cars(scrape())
        old, to_send = storage.load()

        merged, new = merge(old, scraped)
        to_send = to_send + new

        print('Cars to save: ' + str(len(merged)))
        print('New cars: ' + str(len(new)))
        # for avto in new:
        #     print(avto)

        if time() - last_send > config.SEND_INTERVAL:
            mail.send(to_send)
            to_send = []

            last_send = time()

        storage.save(merged[0:1000], to_send)

        sleep(config.SCRAPE_INTERVAL)
