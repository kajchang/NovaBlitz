#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, send_from_directory, request
import glob
import os
import json

app = Flask(__name__)


@app.route('/cards/<card_name>')
def cardsearch(card_name):
    for file_ in glob.glob('cards/*.json'):
        if os.path.basename(file_.lower()).replace('.json', '') == card_name.lower():
            return send_from_directory('cards', os.path.basename(file_))

    return render_template('404.html', card_name=card_name), 404


@app.route('/cards')
def cards():
    return json.dumps([json.load(open(file_)) for file_ in glob.glob('cards/*.json') if os.path.basename(
        file_.lower()).replace('.json', '') in [card.lower() for card in request.args.getlist('cards[]', None)]])


@app.route('/cardlist')
def cardlist():
    return json.dumps([os.path.basename(card).replace(
        '.json', '') for card in glob.glob('cards/*.json')])


if __name__ == '__main__':
    app.run()
