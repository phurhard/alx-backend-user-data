#!/usr/bin/env python3
""" Authentication base"""
from flask import request
from os import getenv
from typing import List, TypeVar


class Auth:
    """Authentication class"""
    def __init__(self):
        """Initialization"""
        self.session_cookie_name = getenv("SESSION_NAME", "_my_session_id")

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns False is a user does not require auth"""
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        elif path in excluded_paths or f'{path}/' in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """Authorization Header"""
        if request is None or "Authorization" not in request.headers:
            return None
        else:
            return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        """Currrent user"""
        return None

    def session_cookie(self, request=None):
        """Returms a cookie value from a request"""
        if request is None:
            return None
        return request.cookies.get(self.session_cookie_name)
