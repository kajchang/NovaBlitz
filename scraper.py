#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

import os

import sqlite3


pages = ['https://novablitz.gamepedia.com/index.php?title=Category:Cards&pageuntil=Nature+Boost#mw-pages',
         'https://novablitz.gamepedia.com/index.php?title=Category:Cards&pagefrom=Nature+Boost#mw-pages']

if not os.path.exists(os.path.join(os.path.dirname(__file__), 'cards.db')):
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'cards.db'))
    c = conn.cursor()
    with open(os.path.join(os.path.dirname(__file__), 'sql/startup.sql')) as script:
        c.execute(script.read())

else:
    conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'cards.db'))
    c = conn.cursor()


for page in pages:
    page = BeautifulSoup(requests.get(page).text, 'html.parser')

    for card in page.find(class_='mw-category').find_all('a'):
        card = BeautifulSoup(requests.get(
            'https://novablitz.gamepedia.com{}'.format(card['href'])).text, 'html.parser'
        )

        card_data = {
            'NAME': ''.join(card.find(class_='title').text.split()).lower(),
            'IMAGE': card.find('img')['src'],
            'CARDTEXT': card.find('p', style='font-weight: bold;').text if card.find('p', style='font-weight: bold;') else None,
            'REALNAME': card.find(class_='title').text
        }

        if card_data['NAME'] == 'demonichorror':
            continue  # NovaBlitz Gamepedia Problem with Demonic Horror Page

        for attr, value in zip(card.find(class_='body').find_all('th'), card.find(class_='body').find_all('td')):
            card_data[attr.text.replace('\n', '').replace(':', '').strip().upper() if attr.text.replace('\n', '').replace(':', '').strip().upper() != 'SET' else 'CARDSET'] = int(value.text.replace(
                '\n', '').strip()) if value.text.replace('\n', '').strip().isdigit() else value.text.replace('\n', '').strip()

        c.execute('INSERT OR REPLACE INTO CARDS {0}\nVALUES ({1}?);'.format(tuple(card_data),
                                                                            '?,' * (len(card_data) - 1)), tuple(card_data.values()))
        conn.commit()

conn.close()
