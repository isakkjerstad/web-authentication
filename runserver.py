#!/usr/bin/python3

from server import create_web_app, config

debug_server = create_web_app()

if __name__ == "__main__":

    debug_server.run(
        debug = config.DEBUG,
        port = config.PORT,
        threaded = config.THREADED
    )