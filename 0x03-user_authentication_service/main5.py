#!/usr/bin/env python3
"""
Main file
"""
from auth import _hash_password

print(_hash_password("Hello Holberton"))
print(_hash_password(2))
print(_hash_password(""))
