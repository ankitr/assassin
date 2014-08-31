#!/usr/bin/env python

import os
from flask import Flask
from flask import render_template

app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def main():
    try:
        with open('../registrations.csv') as f:
            registrants = sum(1 for _ in f) - 1
    except IOError:
        # :O
        registrants = 420
    return render_template('main.html', registrants=registrants)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
