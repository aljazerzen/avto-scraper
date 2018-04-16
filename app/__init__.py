from time import sleep
from app import config, storage, mail
from app.scrape import scrape, merge


def main():
    scraped = scrape()
    old = storage.load()

    merged, new = merge(old, scraped)

    print('Cars to save: ' + str(len(merged)))
    print('New cars: ' + str(len(new)))

    # for avto in new:
    #     print(avto)

    storage.save(merged[0:1000])
    mail.send(new)


def app():
    while True:
        # try:
        main()
        # except Exception as e:
        # with open('error.log', 'a+') as f:
        # f.write(f'\n[{datetime.now()}]:\n' + str(e) + str(e.args) + '\n')
        # f.close()

        sleep(config.SCRAPE_INTERVAL)
