#!/usr/bin/env python3
""" Basic Auth is implemented  here
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic authentication class"""
    def __init__(self):
        """ Basic Initialization"""
        super().__init__()
