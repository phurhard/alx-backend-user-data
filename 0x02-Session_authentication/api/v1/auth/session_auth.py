#!/usr/bin/env python3
""" Session Auth is implemented  here
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
import uuid
from typing import TypeVar


class SessionAuth(Auth):
    """ Session authentication class"""
    def __init__(self):
        """ Session Initialization"""
        super().__init__()

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session id for a user"""
        if user_id is None or not type(user_id) is str:
            return None
        else:
            session_id = uuid.uuid4()
            self.user_id_by_session_id[session_id] = user_id
            return session_id

    def user_id_for_session_id(self, session_id:
                               str = None) -> str:
        """Returns a User id based on session id"""
        if session_id is None or  isinstance(
                session_id, str):
            return None
        ret = self.user_id_by_session_id.get(session_id)
        return ret
