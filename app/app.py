#!/usr/bin/env python

import os

from flask import Flask
from flask import make_response
from flask import render_template
from flask import request

from xml.etree import ElementTree

from utils import get_users
from utils import kill_user
from utils import user_target
from utils import assassin_of

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

@app.route('/c/voice', methods=['POST'])
def voice():
    # Say hi.
    response = ElementTree.Element('Response')
    message = ElementTree.SubElement(response, 'Reject')
    # Stringify
    response = ElementTree.tostring(response)
    # Responsify
    response = make_response(response)
    response.headers['Content-Type'] = 'application/xml'
    return response

@app.route('/c/sms', methods=['POST'])
def sms():
    # NOTE: This uses our makeshift version of a database (a lame csv). One should
    #       consider improving.
    response = ElementTree.Element('Response')
    message = ElementTree.SubElement(response, 'Message')
    sender = request.form['From'][2:]
    command = request.form['Body'].upper()
    users = get_users()
    numbers = [user[3] for user in users]
    if not (sender in numbers):
        message.text = 'Sorry, you are using an unidentified number.'
    else:
        user = next((_ for _ in users if _[3]==sender), None)
        if user[4] != 'True':
            message.text = 'This agent has been eliminated. Contact GM for help.'
        elif command == 'DEAD':
            message.text = 'Thanks for playing! Hope you had fun.'
            kill_user(users.index(user))
            assassin = assassin_of(users.index(user))
            bounty = ElementTree.SubElement(response, 'Message',
                                        attrib={'to':assassin[3]})
            bounty.text = ('Agent %s has been eliminated. Your new target is %s.'
                           ' Good luck.'
                           % (user[0], user_target(users.index(assassin))[0]))
        elif command == 'COMPLETE':
            target = user_target(users.index(user))
            kill_user(users.index(target))
            message.text = ('Congratulations. Your next target is %s. Good luck.'
                            % user_target(users.index(user))[0])
            obituary = ElementTree.SubElement(response, 'Message',
                                          attrib={'to':target[3]})
            obituary.text = ('Sources state you have been eliminated by %s. '
                             'Thanks for playing!') % user[0]
        elif command == 'HELP':
            message.text = 'Available commands: DEAD, COMPLETE.'
        else:
            message.text = ('This is an automated system. Unrecognized command. '
                            'HELP for help.')
    response = ElementTree.tostring(response)
    response = make_response(response)
    response.headers['Content-Type'] = 'application.xml'
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=(port==5000))
