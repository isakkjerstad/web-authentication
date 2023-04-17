#!/usr/bin/python3

from . import database as db
from .config import USRNAME_MAX_LEN

class User(db.Model):
    ''' Users utilize the bcrypt password hashing function for storing passwords. '''

    uuid = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(USRNAME_MAX_LEN), nullable = False, unique = True)
    activated = db.Column(db.Boolean(), default = False)
    password_hash = db.Column(db.BINARY(60), nullable = False)
