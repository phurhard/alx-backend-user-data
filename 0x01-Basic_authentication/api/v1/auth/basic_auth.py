#!/usr/bin/env python3
"""Basic Auth"""
from auth.auth import Auth



class BasicAuth(Auth):
    """Basic autheication class"""
    def __init__(self):
        """Basic Initialization"""
        super().__init__()
