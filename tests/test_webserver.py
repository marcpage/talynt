#!/usr/bin/env python3


import tempfile
import time
import types
import hashlib

from talynt.model import User, Database
from talynt.webserver import create_app, COOKIE
import talynt.sessionkey

ARGS = types.SimpleNamespace(secret='Setec Astronomy', database=None)


def test_root():
    with tempfile.TemporaryDirectory() as workspace:
        ARGS.database = "sqlite:///" + workspace + "test.sqlite3"
        app = create_app(ARGS)
        app.config.update({"TESTING": True})
        client = app.test_client()
        response = client.get("/")
        assert response.status_code == 200, response.status_code
        assert b'Job Description Assistant'.lower() in response.data.lower(), response.data


def test_login_fail():
    with tempfile.TemporaryDirectory() as workspace:
        ARGS.database = "sqlite:///" + workspace + "test.sqlite3"
        app = create_app(ARGS)
        app.config.update({"TESTING": True})
        client = app.test_client()
        response = client.post("/login", data={
            'email': 'john.appleseed@apple.com',
            'password': 'Setec astronomy'
        }, follow_redirects=True)
        assert response.status_code == 200, response.status_code
        assert b'invalid login' in response.data.lower(), response.data


def test_login_success():
    username = "john.appleseed@apple.com"
    password = "Setec astronomy"
    with tempfile.TemporaryDirectory() as workspace:
        ARGS.database = "sqlite:///" + workspace + "test.sqlite3"
        app = create_app(ARGS)
        User.create(username, password)
        app.config.update({"TESTING": True})
        client = app.test_client()
        response = client.post("/login", data={
            'email': username,
            'password': password,
        }, follow_redirects=True)
        assert response.status_code == 200, response.status_code
        assert b'invalid login' not in response.data.lower(), response.data


def test_create_account():
    username = "john.appleseed@apple.com"
    password = "Setec astronomy"
    with tempfile.TemporaryDirectory() as workspace:
        ARGS.database = "sqlite:///" + workspace + "test.sqlite3"
        app = create_app(ARGS)
        app.config.update({"TESTING": True})
        client = app.test_client()
        response = client.post("/create_account", data={
            'email': username,
            'password': password,
            'password_2': password,
        }, follow_redirects=True)
        assert response.status_code == 200, response.status_code
        assert b'invalid login' not in response.data.lower(), response.data
        assert b'logout' in response.data.lower(), response.data
        assert b'/login' not in response.data.lower(), response.data


def test_create_account_fail():
    username = "john.appleseed@apple.com"
    password = "Setec astronomy"
    with tempfile.TemporaryDirectory() as workspace:
        ARGS.database = "sqlite:///" + workspace + "test.sqlite3"
        app = create_app(ARGS)
        User.create(username, password)
        app.config.update({"TESTING": True})
        client = app.test_client()
        response = client.post("/create_account", data={
            'email': username,
            'password': password,
            'password_2': password,
        }, follow_redirects=True)
        assert response.status_code == 200, response.status_code
        assert b'invalid login' in response.data.lower(), response.data
        assert b'logout' not in response.data.lower(), response.data
        assert b'/login' in response.data.lower(), response.data


def test_create_account_bad_password():
    username = "john.appleseed@apple.com"
    password = "Setec astronomy"
    with tempfile.TemporaryDirectory() as workspace:
        ARGS.database = "sqlite:///" + workspace + "test.sqlite3"
        app = create_app(ARGS)
        User.create(username, password)
        app.config.update({"TESTING": True})
        client = app.test_client()
        response = client.post("/create_account", data={
            'email': username,
            'password': password,
            'password_2': password+" ",
        }, follow_redirects=True)
        assert response.status_code == 200, response.status_code
        assert b'invalid login' in response.data.lower(), response.data
        assert b'logout' not in response.data.lower(), response.data
        assert b'/login' in response.data.lower(), response.data


def test_bad_session_password():
    while time.localtime().tm_min == 59:
        time.sleep(0.100)  # To prevent test flakiness around hour changes

    with tempfile.TemporaryDirectory() as workspace:
        ARGS.database = "sqlite:///" + workspace + "test.sqlite3"
        app = create_app(ARGS)
        User.create("john.appleseed@apple.com", "Setec astronomy")
        app.config.update({"TESTING": True})
        client = app.test_client()
        user = types.SimpleNamespace(id=1, password_hash=hashlib.sha256("password".encode()).hexdigest())
        headers = {'User-Agent': 'Chrome'}
        bad_session = talynt.sessionkey.create(user.id, user.password_hash, headers, ARGS.secret)
        client.set_cookie(domain='localhost', key=COOKIE, value=bad_session)
        response = client.get("/", headers=headers)
        assert response.status_code == 200, response.status_code
        assert b'logout' in response.data.lower(), response.data
        assert b'/login' not in response.data.lower(), response.data


def test_404():
    with tempfile.TemporaryDirectory() as workspace:
        ARGS.database = "sqlite:///" + workspace + "test.sqlite3"
        app = create_app(ARGS)
        app.config.update({"TESTING": True})
        client = app.test_client()
        response = client.get("/not_found")
        assert response.status_code == 404, response.status_code
        assert b'not found' in response.data.lower(), response.data


def test_logout():
    with tempfile.TemporaryDirectory() as workspace:
        ARGS.database = "sqlite:///" + workspace + "test.sqlite3"
        app = create_app(ARGS)
        User.create("john.appleseed@apple.com", "Setec astronomy")
        app.config.update({"TESTING": True})
        client = app.test_client()
        response = client.post("/login", data={
            'email': 'john.appleseed@apple.com',
            'password': 'Setec astronomy'
        }, follow_redirects=True)
        assert response.status_code == 200, response.status_code
        assert b'invalid login' not in response.data.lower(), response.data
        assert client.get_cookie(COOKIE)
        response = client.get("/logout", follow_redirects=True)
        assert response.status_code == 200, response.status_code
        assert b'logout' not in response.data.lower(), response.data
        assert b'/login' in response.data.lower(), response.data
        assert not client.get_cookie(COOKIE), client.get_cookie(COOKIE)


if __name__ == "__main__":
    test_root()
    test_login_fail()
    test_login_success()
    test_bad_session_password()
    test_404()
    test_logout()
    test_create_account_fail()
    test_create_account()
    test_create_account_bad_password()
