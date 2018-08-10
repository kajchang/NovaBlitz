#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import (Flask, render_template, redirect,
                   request, jsonify)
import os
import sqlite3

app = Flask(__name__)


def reconstruct_card(data_tuple):
    return {'name': data_tuple[1],
            'cost': data_tuple[2],
            'type': data_tuple[3],
            'set': data_tuple[4],
            'rarity': data_tuple[5],
            'aspect': data_tuple[6],
            'image': data_tuple[7],
            'text': data_tuple[8],
            'subtype': data_tuple[9],
            'attack': data_tuple[10],
            'health': data_tuple[11]}


@app.route('/')
def main():
    return redirect('https://documenter.getpostman.com/view/4967569/RWTivyzL'), 301


@app.route('/cards/<card_name>')
def cardsearch(card_name):
    with sqlite3.connect(os.path.join(os.path.dirname(__file__), 'cards.db')) as conn:
        c = conn.cursor()
        card = c.execute(
            'SELECT * FROM "CARDS" WHERE "NAME" = ?', (card_name.lower(),)).fetchone()
        if card is None:
            return render_template('404.html', card_name=card_name), 404

        else:
            return jsonify(reconstruct_card(card))


@app.route('/cards')
def cards():
    with sqlite3.connect(os.path.join(os.path.dirname(__file__), 'cards.db')) as conn:
        c = conn.cursor()
        card_names = [card_name.lower()
                      for card_name in request.args.getlist('cards[]', None)]
        return jsonify([reconstruct_card(card) for card in c.execute('SELECT * FROM "CARDS" WHERE "NAME" IN ({0}?)'.format('?,' * (len(card_names) - 1)), tuple(card_names)).fetchall()])


@app.route('/cardlist')
def cardlist():
    with sqlite3.connect(os.path.join(os.path.dirname(__file__), 'cards.db')) as conn:
        c = conn.cursor()
        return jsonify([name[0] for name in c.execute('SELECT "NAME" FROM "CARDS"').fetchall()])


if __name__ == '__main__':
    app.run()
