from flask import Flask, render_template, send_from_directory
import glob

app = Flask(__name__)


@app.route('/cards/<card_name>')
def cards(card_name):
    for file in glob.glob('cards/*.json'):
        if file[6:-5].lower() == card_name.lower():
            return send_from_directory('cards', file[6:])

    return render_template('404.html', card_name=card_name), 404


if __name__ == '__main__':
    app.run()
