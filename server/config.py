#!/usr/bin/python3

# General settings.
DATABASE_NAME = "db.sqlite3"
USRNAME_MIN_LEN = 1
USRNAME_MAX_LEN = 255
MIN_PASSWD_LEN = 8

# Exponential factor that makes it slower to compute the hash (4 to 31).
HASH_COST = 12

# Relative path to the disallowed password list in JSON format.
DISALLOWED_PASSWORD_LIST_PATH = "server/static/PwnedPasswordsTop100k.json"

# Server API key.
API_KEY = "36!fs@s63gc%"

# Debug server settings.
DEBUG = True
THREADED = True
HOST = "localhost"
PORT = 8080

# HTTP error codes.
HTTP_400_BAD_REQUEST = 400
HTTP_500_INTERNAL_SERVER_ERROR = 500
