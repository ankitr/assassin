#!/usr/bin/env python

import csv

def get_users():
    # Such a hack. I didn't even check if it was an iterable.
    users = []
    with open('../randomized.csv') as db:
        try:
            reader = csv.reader(db)
            for row in reader:
                users.append(row)
        finally:
            db.close()
    return users

def kill_user(i):
    users = get_users()
    users[i][4] = False
    with open('../randomized.csv', 'wb+') as db:
        writer = csv.writer(db)
        writer.writerows(users)

# TODO: Consider abstracting the following.

def user_target(i):
    users = get_users()
    pivot = users[i+1:] + users[:i]
    return _survivor(pivot)

def assassin_of(i):
    users = get_users()
    pivot = (users[i+1:] + users[:i])[::-1]
    return _survivor(pivot)
    
def _survivor(pivot):
    boss = ['Ankit Ranjan', 'Ankit', 'me@ankit.io', '1234567', 'True']
    return next((_ for _ in pivot if _[4]=='True'), boss)
