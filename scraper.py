#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import os
import json


pages = ['https://novablitz.gamepedia.com/index.php?title=Category:Cards&pageuntil=Nature+Boost#mw-pages',
         'https://novablitz.gamepedia.com/index.php?title=Category:Cards&pagefrom=Nature+Boost#mw-pages']


if not os.path.exists('cards'):
    os.makedirs('cards')

for page in pages:
    page = BeautifulSoup(requests.get(page).text, 'html.parser')

    for card in page.find(class_='mw-category').find_all('a'):
        card = BeautifulSoup(requests.get(
            'https://novablitz.gamepedia.com{}'.format(card['href'])).text, 'html.parser'
        )

        card_data = {
            'name': card.find(class_='title').text,
            'image': card.find('img')['src'],
            'text': card.find('p', style='font-weight: bold;').text if card.find('p', style='font-weight: bold;') else None,
        }

        for attr, value in zip(card.find(class_='body').find_all('th'), card.find(class_='body').find_all('td')):
            card_data[attr.text.replace('\n', '').replace(':', '').strip().lower()] = int(value.text.replace(
                '\n', '').strip()) if value.text.replace('\n', '').strip().isdigit() else value.text.replace('\n', '').strip()

        with open('cards/{}.json'.format(card.find(class_='title').text.replace(' ', '')), 'w') as card_file:
            card_file.write(json.dumps(card_data))
