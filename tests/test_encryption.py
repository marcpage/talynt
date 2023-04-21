#!/usr/bin/env python3


import time
import hashlib
import types

from talynt.encryption import encrypt, decrypt


def test_basic():
    test_cases = [(f"{i}"*i).encode('utf-8') for i in range(0, 256)]
    test_keys = [f"{i}"*i for i in range(0, 256)]

    for test_key in test_keys:
        for test_case in test_cases:
            encrypted = encrypt(test_key, test_case)
            decrypted = decrypt(test_key, encrypted)
            assert test_case == decrypted, f"key = '{test_key}' value = '{test_case}'"


if __name__ == "__main__":
    test_basic()
