#!/usr/bin/python3

from . import database as db
from .config import USRNAME_MAX_LEN

class User(db.Model):

    uuid = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(USRNAME_MAX_LEN), nullable = False, unique = True)
    password_hash = db.Column(db.String(512), nullable = False)
