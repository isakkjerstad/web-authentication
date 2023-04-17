#!/usr/bin/python3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import DATABASE_NAME
from os import path, remove

database = SQLAlchemy()

def create_web_app():

    web_app = Flask(__name__)

    # Flask configuration.
    web_app.config.update(
        SECRET_KEY = "HWiZ7Ft3fTy9Y54enng2PgnUcmqBFNVo",
        SEND_FILE_MAX_AGE_DEFAULT = 0,
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_NAME}",
        SQLALCHEMY_TRACK_MODIFICATIONS = False,
    )

    # Set up the database.
    database.init_app(web_app)
    from . import models
    create_database(web_app)

    # Register views.
    from .views import views
    web_app.register_blueprint(views, url_prefix = "/")

    return web_app

def create_database(web_app):
    ''' Create a new database if non-existent. '''

    with web_app.app_context():
        database.create_all()
        print(" * Initialized database!")

def delete_database():
    ''' Deletes the database if it exists. '''
    
    # Newer versions of flask.
    if path.exists("instance/" + DATABASE_NAME):
        remove("instance/" + DATABASE_NAME)
        print(" * Database deleted!")

    # Old versions of flask (not supported).
    elif path.exists(__name__ + "/" + DATABASE_NAME):
        remove(__name__ + "/" + DATABASE_NAME)
        print(" * Database deleted!")
