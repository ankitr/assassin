#!/usr/bin/env python

# WARNING: Extreme hackiness below! Proceed with caution (and duct tape).

import csv

from twilio.rest import TwilioRestClient 

# Get our users.
users = []
with open('../../randomized.csv') as f:
	try:
		reader = csv.reader(f)  # creates the reader object
		for row in reader:   # iterates the rows of the file in orders
			print row
			users.append(row)
	finally:
		f.close()      # closing
targets = users[1:] + users[:1]

# Omitted in commit 
ACCOUNT_SID = ""
AUTH_TOKEN = "" 

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 

for i in xrange(len(users)):
	user = users[i][0]
	number = users[i][3]
	target = targets[i][0]
	if number:
		print 'Texting %s' % user
		client.messages.create(
			to=number,
			from_="+16502414303",
			body="Good evening Agent %s. Your mission, if you choose to accept it, is to eliminate %s. Contact the GM if you need more info. Good luck!" % (user, target)
		)
	else:
		print 'Not texting %s' % user
