import certifi
import urllib3
from bs4 import BeautifulSoup


def scrape():
    quote_page = 'https://www.avto.net/Ads/results_100.asp'

    http = urllib3.PoolManager(
        cert_reqs='CERT_REQUIRED',
        ca_certs=certifi.where())
    r = http.request('GET', quote_page)

    soup = BeautifulSoup(r.data, 'html.parser')

    results = soup.find_all('div', attrs={'class': 'ResultsAd'})

    avti = []

    for result in results:

        data = result.find('div', attrs={'class': 'ResultsAdData'})

        avto = {
            'id': data.find('a', attrs={'class': 'Adlink'})['href'].split('id=')[1].split('&')[0],
            'name': data.span.text,
            'cena': result.find('div', attrs={'class': 'ResultsAdPrice'}).text.strip().split(' €')[0]
        }

        for a in data.ul.children:
            if a.name:
                if 'Letnik 1.registracije:' in a.text:
                    avto['reg'] = a.text.split(':')[1]
                elif ' km' in a.text:
                    avto['km'] = int(a.text.split(' km')[0])
                elif 'motor, ' in a.text:
                    avto['motor'] = a.text
                elif 'menjalnik' in a.text:
                    avto['menjalnik'] = a.text

        avti.append(avto)
    return avti


def merge(old_cars, new_cars):
    new = []
    merged = []
    for newAvto in new_cars:
        if len(old_cars) > 0 and newAvto['id'] == old_cars[0]['id']:
            old_cars.pop(0)
        else:
            new.append(newAvto)
        merged.append(newAvto)

    merged = merged + old_cars
    return merged, new
