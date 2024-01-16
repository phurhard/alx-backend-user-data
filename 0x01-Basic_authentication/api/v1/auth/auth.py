#!/usr/bin/env python3
""" Authentication base"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Authentication class"""
    def __init__(self):
        """Initialization"""
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Returns False is a user does not require auth"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True

        elif path in excluded_paths or path+'/' in excluded_paths:
            return False
        for patterns in excluded_paths:
            if patterns.endswith('*') and path.startswith(patterns[:-1]):
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
