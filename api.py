#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import (Flask, render_template,
                   send_from_directory, request, make_response, jsonify)
import glob
import os

app = Flask(__name__)


@app.route('/cards/<card_name>')
def cardsearch(card_name):
    for file_ in glob.glob('cards/*.json'):
        if os.path.basename(file_.lower()).replace('.json', '') == card_name.lower():
            resp = make_response(send_from_directory(
                'cards', os.path.basename(file_)))
            resp.headers['Content-Type'] = 'application/json'

            return resp

    return render_template('404.html', card_name=card_name), 404


@app.route('/cards')
def cards():
    resp = make_response(jsonify([json.load(open(file_)) for file_ in glob.glob('cards/*.json') if os.path.basename(
        file_.lower()).replace('.json', '') in [card.lower() for card in request.args.getlist('cards[]', None)]]))
    resp.headers['Content-Type'] = 'application/json'

    return resp


@app.route('/cardlist')
def cardlist():
    resp = make_response(jsonify([os.path.basename(card).replace(
        '.json', '') for card in glob.glob('cards/*.json')]))
    resp.headers['Content-Type'] = 'application/json'

    return resp


if __name__ == '__main__':
    app.run()
