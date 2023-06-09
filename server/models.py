#!/usr/bin/python3

from . import database as db
from sqlalchemy.sql import func
from .config import USRNAME_MAX_LEN

class User(db.Model):
    ''' Users utilize the bcrypt password hashing function for storing passwords. '''

    uuid = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(USRNAME_MAX_LEN), nullable = False, unique = True)
    activated = db.Column(db.Boolean(), default = False)
    password_hash = db.Column(db.BINARY(60), nullable = False)

class SensorData(db.Model):
    '''
    Sensor data for a Bosch BME680 sensor.

    id          -> unique datapoint ID.
    time        -> datetime object.
    location    -> string from sensor describing the sensor placement.
    temperature -> temperature in degrees celsius (-40 to 85°C).
    pressure    -> barometric pressure in hectopascals (300 to 1100 hPa).
    humidity    -> relative humidity in percent (0 to 100%).
    aqi         -> Air Quality Index, abstract number.
    '''

    id = db.Column(db.Integer, primary_key = True)
    time = db.Column(db.DateTime(timezone = True), server_default = func.now())
    location = db.Column(db.String(64), nullable = False)
    temperature = db.Column(db.Float, nullable = False)
    pressure = db.Column(db.Float, nullable = False)
    humidity = db.Column(db.Float, nullable = False)
    aqi = db.Column(db.Float, nullable = False)
