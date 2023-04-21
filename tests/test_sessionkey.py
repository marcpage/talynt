#!/usr/bin/env python3


import time
import hashlib
import types
import datetime
import base64

from talynt.sessionkey import create, parse
from talynt.encryption import encrypt


def test_basic():
    while time.localtime().tm_min == 59:
        time.sleep(0.100)  # To prevent test flakiness around hour changes

    secret = "Setec astronomy"
    user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3"
    user_id = 5
    user_pwhash = hashlib.sha256("password".encode()).hexdigest()
    headers = {'User-Agent': user_agent}

    key = create(user_id, user_pwhash, headers, secret)
    uid, password_hash = parse(key, headers, secret)
    assert uid == user_id, f"user_id: {user_id} uid: {uid}"
    assert password_hash == user_pwhash, f"user_pwhash: {user_pwhash} password_hash: {password_hash}"


def test_old():
    while time.localtime().tm_min == 59:
        time.sleep(0.100)  # To prevent test flakiness around hour changes

    secret = "Setec astronomy"
    user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3"
    user_id = 5
    user_pwhash = hashlib.sha256("password".encode()).hexdigest()
    headers = {'User-Agent': user_agent}

    key = create(user_id, user_pwhash, headers, secret, hour_delta=-1)
    uid, password_hash = parse(key, headers, secret)
    assert uid == user_id, f"user_id: {user_id} uid: {uid}"
    assert password_hash == user_pwhash, f"user_pwhash: {user_pwhash} password_hash: {password_hash}"


def test_bad():
    while time.localtime().tm_min == 59:
        time.sleep(0.100)  # To prevent test flakiness around hour changes

    secret = "Setec astronomy"
    user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3"
    user_id = 5
    user_pwhash = hashlib.sha256("password".encode()).hexdigest()
    headers = {'User-Agent': user_agent}

    key = create(user_id, user_pwhash, headers, secret, hour_delta=+1)
    user_id, password_hash = parse(key, headers, secret)
    assert user_id is None, f"user_id: {user_id}"
    assert password_hash is None, f"password_hash: {password_hash}"


def test_bad_unicode():
    while time.localtime().tm_min == 59:
        time.sleep(0.100)  # To prevent test flakiness around hour changes

    now = datetime.datetime.now()
    hour_string = now.strftime("%Y/%m/%d@%H")
    secret = "Setec astronomy"
    user_agent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3"
    headers = {'User-Agent': user_agent}
    key_data = f"{secret}:{hour_string}:{headers['User-Agent']}"
    utf8_first_continuation_byte = b'\x80, \xC0, \xC1, \xF5..\xFF'  # invalid utf-8 string
    bad_session = encrypt(key_data, utf8_first_continuation_byte)
    bad_key = base64.b64encode(bad_session).decode("utf-8")
    user_id, password_hash = parse(bad_key, headers, secret)
    assert user_id is None
    assert password_hash is None

if __name__ == "__main__":
    test_basic()
    test_old()
    test_bad()
    test_bad_unicode()
