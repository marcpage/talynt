#!/usr/bin/env python3

"""
    Main entrypoint to web server
"""


import argparse

import talynt.webserver


DEFAULT_WEB_PORT = 8000
DEFAULT_DATABASE = "talynt.sqlite3"


def parse_command_line():
    """Parses command line options"""
    parser = argparse.ArgumentParser(
        description="A web-based job description evaluator"
    )
    parser.add_argument(
        "-p",
        "--port",
        dest="port",
        type=int,
        help=f"The port the web server listens on ({DEFAULT_WEB_PORT})",
    )
    parser.add_argument(
        "-d",
        "--db",
        dest="database",
        type=str,
        help="path to Sqlite3 database " + f"({DEFAULT_DATABASE})",
    )
    parser.add_argument(
        "--secret",
        dest="secret",
        type=str,
        help="The secret phrase used to encrypt session tokens",
    )
    parser.add_argument(
        "--debug", dest="debug", action="store_true", help="Should we be debugging"
    )
    return parser.parse_args()


def main(args=parse_command_line()):
    """main entrypoint"""
    app = talynt.webserver.create_app(args)

    try:
        app.run(host="0.0.0.0", debug=args.debug, port=args.port)

    except KeyboardInterrupt:
        pass  # cleanup


if __name__ == "__main__":
    main(parse_command_line())
