from datetime import datetime
from time import sleep
import certifi
import urllib3
import yaml
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from string import Template

f = open('config.yaml','r') 
config = yaml.load(f)
f.close()

def scrapePage():

	quote_page = 'https://www.avto.net/Ads/results_100.asp'

	http = urllib3.PoolManager(
		cert_reqs='CERT_REQUIRED',
	    ca_certs=certifi.where())
	r = http.request('GET', quote_page)

	soup = BeautifulSoup(r.data, 'html.parser')

	results = soup.find_all('div', attrs={'class': 'ResultsAd'})

	avti = [];

	for result in results:
		
		data = result.find('div', attrs={'class': 'ResultsAdData'})

		avto = {}

		avto['id'] = data.find('a', attrs={'class': 'Adlink'})['href'].split('id=')[1].split('&')[0]
		avto['name'] = data.span.text
		avto['cena'] = result.find('div', attrs={'class': 'ResultsAdPrice'}).text.strip().split(' €')[0]

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

def loadStorage():

	try:
		f = open('avti.yaml','r') 
	except FileNotFoundError:
		return []
	
	res = yaml.load(f)
	f.close()
	return res['avti'] if (res is not None and 'avti' in res) else []

def saveStorage(avti):

	f = open('avti.yaml','w') 
	
	f.write(yaml.dump({ 'avti': avti }))
	f.close()

def merge(oldAvti, newAvti):
	new = []
	merged = []
	for newAvto in newAvti:
		if len(oldAvti) > 0 and newAvto['id'] == oldAvti[0]['id']:
			oldAvti.pop(0)
		else:
			new.append(newAvto)
		merged.append(newAvto)
	
	merged = merged + oldAvti
	return merged, new

def sendMail(newCars):
	global config, carPageUrl
	conf = config['smtp']

	text = 'Nove objave na Avto.net:<br><ul style="line-height: 2em;">'
	templateStr = '<li><a href="https://www.avto.net/Ads/details.asp?id=${id}">${name}</a><br>${cena} €, letnik: 2008, ${km} km</li>'
	for car in newCars:
		if 'km' not in car:
			car['km'] = '?'
		text += Template(templateStr).substitute(car)

	text += '</ul>'

	msg = MIMEText(text, 'html')
	
	# print(text)

	msg['Subject'] = 'Nove objave na Avto.net (' + str(len(newCars)) + ')'
	msg['From'] = conf['from']
	msg['To'] = conf['to']

	s = smtplib.SMTP(conf['host'], conf['port'])
	s.login(conf['user'], conf['password'])
	# s.sendmail(conf['from'], [conf['to']], msg.as_string())
	s.quit()


def main():
	scraped = scrapePage()
	old = loadStorage()

	merged, new = merge(old, scraped)

	print('Cars to save: ' + str(len(merged)))
	print('New cars: ' + str(len(new)))

	# for avto in new:
		# print(avto)

	saveStorage(merged[0:1000])
	sendMail(new)

while True:
    # try:
    main()
    # except Exception as e:
        # with open('error.log', 'a+') as f:
            # f.write(f'\n[{datetime.now()}]:\n' + str(e) + str(e.args) + '\n')
            # f.close()

    sleep(config['app']['interval'])
