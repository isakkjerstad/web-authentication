#!/usr/bin/python3

import sys
from server import create_web_app, config, delete_database

if __name__ == "__main__":

    # Delete database before creating a new one upon a full system reset.
    if "-r" in sys.argv[1:] or "--reset" in sys.argv[1:]:
        delete_database()

    debug_server = create_web_app()

    debug_server.run(
        debug = config.DEBUG,
        port = config.PORT,
        threaded = config.THREADED,
        host = config.HOST,
    )
