#!/usr/bin/env python3
""" Basic Auth is implemented  here
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ Basic authentication class"""
    def __init__(self):
        """ Basic Initialization"""
        super().__init__()

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Returns the base64 part of a basic Auth"""
        if authorization_header is None or not isinstance(authorization_header,
           str) or not authorization_header.startswith("Basic "):
            return None
        else:
            return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """Returns the decoded base64 auth header"""
        if base64_authorization_header is None or not\
           isinstance(base64_authorization_header, str):
            return None
        try:
            decode = base64.b64decode(base64_authorization_header)
            return decode.decode('utf-8')
        except Exception as e:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Extracts the users details from the basic auth"""
        if decoded_base64_authorization_header is None or not\
           isinstance(decoded_base64_authorization_header, str)\
           or not decoded_base64_authorization_header.__contains__(':'):
            return (None, None)
        else:
            user, password = decoded_base64_authorization_header.split(':')
            return (user, password)

    def user_object_from_credentials(self, user_email: str, user_pwd:
                                     str) -> TypeVar('User'):
        """Returns a user based on his credentials"""
        if user_email is None or not isinstance(user_email, str)\
           or user_pwd is None or not isinstance(user_pwd, str):
            return None
        else:
            user = User.search({'email': user_email})
            if len(user) == 0:
                return None
            elif not user[0].is_valid_password(user_pwd):
                return None
            else:
                return user[0]

    def current_user(self, request=None) -> TypeVar('User'):
        """Overloads Auth"""
        if request is not None:
            Authorization_header = request.headers['Authorization']
            extractedAuthHeader = self.extract_base64_authorization_header(
                    Authorization_header)
            decodedHeader = self.decode_base64_authorization_header(
                    extractedAuthHeader)
            usermail, pwd = self.extract_user_credentials(decodedHeader)
            user = self.user_object_from_credentials(usermail, pwd)
            return user
