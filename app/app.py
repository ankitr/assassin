#!/usr/bin/env python

import os

from flask import Flask
from flask import make_response
from flask import render_template

from xml.etree import ElementTree

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

@app.route('/voice')
def voice():
    # Say hi.
    response = ElementTree.Element('Response')
    message = ElementTree.SubElement(response, 'Say', attrib={'voice':'alice'})
    message.text = ('Hello, agent. This number has been deprecated for all voice'
                    ' transmissions. Please contact the game master with any '
                    'further concerns.')
    # Stringify
    response = ElementTree.tostring(response)
    # Responsify
    response = make_response(response)
    response.headers['Content-Type'] = 'application/xml'
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=(port==5000))
