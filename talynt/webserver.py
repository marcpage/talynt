#!/usr/bin/env python3

""" Root webserver
"""


import flask
from flask import request

import talynt.sessionkey
import talynt.template


COOKIE = "session_id"  # name of the cookie that contains the session key


def get_user(request, args):
    """Determines the user (or None) that is requesting the page"""
    if COOKIE in request.cookies:
        user_id, password_hash = talynt.sessionkey.parse(
            request.cookies[COOKIE],
            request.headers,
            args.secret,
        )

        return user_id, password_hash

    return None, None


def none_if_empty(value: str) -> str:
    """Returns None if value is empty or None, the value otherwise"""
    return value if value else None


def create_app(args):
    """create the flask app"""
    app = flask.Flask(__name__)

    # Mark: Root

    @app.route("/")
    def home(message=None):
        """default location for the server, home"""
        user_id, password_hash = get_user(flask.request, args)

        contents = talynt.template.render(
            "templates/home.html.mako",
            message=message,
            user_id=user_id,
            password_hash=password_hash,
        )

        return contents, 200

    @app.route("/add_job_posting")
    def home():
        contents = talynt.template.render(
            "templates/home.html.mako",
            message=message,
            user_id=user_id,
            password_hash=password_hash,
        )

    @app.route("/login_failed")
    def invalid_login():
        return home(message="Invalid Login")

    # Mark: API

    @app.route("/logout")
    def logout():
        response = flask.make_response(flask.redirect(flask.url_for("home")))
        response.set_cookie(COOKIE, "", expires=0)
        return response

    @app.route("/login", methods=["POST"])
    def login():
        response = flask.make_response(flask.redirect(flask.url_for("home")))
        session_key = talynt.sessionkey.create(
            1, "password", flask.request.headers, args.secret
        )
        response.set_cookie(COOKIE, session_key)
        return response

    # Mark: errors

    @app.errorhandler(404)
    def page_not_found(error=None):
        """Returns error page 404"""
        return f"<html><body>404 not found<p>{error}</p></body></html>", 404

    return app
