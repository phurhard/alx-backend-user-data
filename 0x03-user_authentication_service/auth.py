#!/usr/bin/env python3
'''Authentication'''
import bcrypt
from user import User
from db import DB


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        '''initialization'''
        self._db = DB()
    
    @property
    def _hash_password(self, pwd: str) -> bin:
        '''Takes a string and returns a binary'''
        salt = bcrypt.gensalt()
        passwd = pwd.encode('utf-8')
        return bcrypt.hashpw(passwd, salt)

    def register_user(self, mail: str, password: str):
        '''Registers a new user'''
        user = self._db._session.query(User).filter_by(email=mail).first()
        if user is None:
            newUser = User()
            newUser.email = mail
            newUser.password = self._hash_password(password)
            self._db._session.add(newUser)
            self._db._session.commit()
            return newUser
        else:
            raise ValueError(f"User {mail} already exists")
