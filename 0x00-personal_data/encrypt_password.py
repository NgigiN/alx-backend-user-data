#!/usr/bin/env python3
"""Module for encrypting passwords"""

import bcrypt


def hash_password(password: str) -> bytes:
    """This function takes password as a string
     salts it, hashes it and then returns a byte
     string
     """
    encoded_pwd = password.encode('utf-8')
    return bcrypt.hashpw(encoded_pwd, bcrypt.gensalt(rounds=12))


def is_valid(hashed_password: bytes, password: str) -> bool:
    """This function verifies the password against its hash"""
    encoded_pwd = password.encode('utf-8')
    if bcrypt.checkpw(encoded_pwd, hashed_password):
        return True
    else:
        return False
