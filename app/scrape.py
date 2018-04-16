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

    cars = []

    for result in results:

        data = result.find('div', attrs={'class': 'ResultsAdData'})

        price = result.find('div', attrs={'class': 'ResultsAdPrice'}).text.strip().split(' €')[0].split(' ')[-1]
        try:
            price = float(price.replace(".", ""))
        except ValueError:
            price = None

        car = {
            'id': data.find('a', attrs={'class': 'Adlink'})['href'].split('id=')[1].split('&')[0],
            'name': data.span.text,
            'price': price,
            'photo': result.find('div', attrs={'class': 'ResultsAdPhotoContainer'}).img['src']
        }

        for a in data.ul.children:
            if a.name:
                if 'Letnik 1.registracije:' in a.text:
                    car['reg'] = a.text.split(':')[1]
                elif ' km' in a.text:
                    car['km'] = int(a.text.split(' km')[0])
                elif 'motor, ' in a.text:
                    car['engine'] = a.text
                elif 'menjalnik' in a.text:
                    car['trans'] = a.text

        if 'km' not in car:
            car['km'] = None

        if 'reg' not in car:
            car['reg'] = None

        cars.append(car)
    return cars
