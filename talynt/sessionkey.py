#!/usr/bin/env python3

""" Handles creating and parsing session keys
"""


import base64
import datetime
import re

import talynt.encryption


SESSION_PATTERN = re.compile(r"^(\d+):([0-9a-fA-F]+)$")


def create(
    user_id: int, user_pwhash: str, headers: dict, secret: str, hour_delta: int = 0
):
    """Creates a session key given the headers and a secret"""
    now = datetime.datetime.now()
    now += datetime.timedelta(hours=hour_delta)
    hour_string = now.strftime("%Y/%m/%d@%H")
    data = f"{user_id}:{user_pwhash}"
    key_data = f"{secret}:{hour_string}:{headers['User-Agent']}"
    encrypted = talynt.encryption.encrypt(key_data, data.encode("utf-8"))
    return base64.b64encode(encrypted).decode("utf-8")


# TODO: Return a refreshed session key if its old  # pylint: disable=fixme
def parse(session_key: str, headers: dict, secret: str, hour_delta: int = 0):
    """Parses a session key given the headers and a secret"""
    now = datetime.datetime.now()
    now += datetime.timedelta(hours=hour_delta)
    hour_string = now.strftime("%Y/%m/%d@%H")
    encrypted = base64.b64decode(session_key)
    key_data = f"{secret}:{hour_string}:{headers['User-Agent']}"
    decrypted = talynt.encryption.decrypt(key_data, encrypted)

    try:
        session_format = SESSION_PATTERN.match(decrypted.decode("utf-8"))

        if session_format:
            return (int(session_format.group(1)), session_format.group(2))

    except UnicodeDecodeError:
        pass

    if hour_delta < 0:
        return (None, None)

    return parse(session_key, headers, secret, hour_delta=-1)
