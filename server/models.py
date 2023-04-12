#!/usr/bin/python3

from . import database as db

class User(db.Model):

    uuid = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255), unique = True)
    password_hash = db.Column(db.String(512))

class Session(db.Model):

    id = db.Column(db.Integer, primary_key = True)
