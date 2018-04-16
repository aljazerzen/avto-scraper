import smtplib
from email.mime.text import MIMEText
from string import Template
from app.config import SMTP


def send(cars):
    if len(cars) == 0:
        return

    text = 'Nove objave na Avto.net:<br><ul style="line-height: 2em;">'
    template_str = '<li><a href="https://www.avto.net/Ads/details.asp?id=${id}">${name}</a><br>' \
                   '${cena} €, letnik: 2008, ${km} km</li>'
    for car in cars:
        if 'km' not in car:
            car['km'] = '?'
        text += Template(template_str).substitute(car)

    text += '</ul>'

    msg = MIMEText(text, 'html')

    msg['Subject'] = 'Nove objave na Avto.net (' + str(len(cars)) + ')'
    msg['From'] = SMTP['from']
    msg['To'] = SMTP['to']

    if SMTP['host'] is not None:
        s = smtplib.SMTP(SMTP['host'], SMTP['port'])
        s.login(SMTP['user'], SMTP['password'])
        s.sendmail(SMTP['from'], [SMTP['to']], msg.as_string())
        s.quit()
    else:
        print("Mail not configured. Should send \"" + text + "\"")
