#!/usr/bin/env python3
"""
Defines hash_password function.
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash the given password.
    """
    return (bcrypt.hashpw(bytes(password, "utf-8"), bcrypt.gensalt(14)))


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Check if a password is correct.
    """
    return (bcrypt.checkpw(bytes(password, "utf-8"), hashed_password))
