from threading import Thread
from time import sleep, time
from app import config, storage, mail, web_app, settings
from app.filter import filter_cars
from app.scrape import scrape
from app.car_service import merge


def scraper():
    last_send = 0

    while True:
        sett = settings.load()

        scraped = filter_cars(scrape())
        old, to_send = storage.load()

        merged, new = merge(old, scraped)
        to_send = to_send + new

        # print('Cars to save: ' + str(len(merged)))
        # print('New cars: ' + str(len(new)))
        # for avto in new:
        #     print(avto)

        if time() - last_send > sett['send_interval']:
            mail.send(to_send)
            to_send = []

            last_send = time()

        storage.save(merged[0:1000], to_send)

        sleep(sett['scrape_interval'])


def app():
    thread = Thread(target=scraper)
    thread.start()

    web_app.app.run(debug=True)
