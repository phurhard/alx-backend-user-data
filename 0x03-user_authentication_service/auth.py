#!/usr/bin/env python3
'''Authentication'''
import bcrypt
from user import User
from db import DB
import uuid


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        '''initialization'''
        self._db = DB()

    def _hash_password(self, pwd: str) -> bin:
        '''Takes a string and returns a binary'''
        salt = bcrypt.gensalt()
        passwd = pwd.encode('utf-8')
        return bcrypt.hashpw(passwd, salt)

    def _generate_uuid(self) -> uuid:
        '''Generate a uuid'''
        return str(uuid.uuid4())

    def register_user(self, mail: str, password: str) -> User:
        '''Registers a new user'''
        user = self._db._session.query(User).filter_by(email=mail).first()
        if user is None:
            newUser = User()
            newUser.email = mail
            newUser.hashed_password = self._hash_password(password)
            self._db._session.add(newUser)
            self._db._session.commit()
            return newUser
        else:
            raise ValueError(f"User {mail} already exists")

    def valid_login(self, mail: str, pwd: str) -> bool:
        '''Validates a user login'''
        user = self._db._session.query(User).filter_by(email=mail).first()
        if user is not None:
            pwd = pwd.encode('utf--8')
            return bcrypt.checkpw(pwd, user.hashed_password)
        else:
            return False

    def create_session(self, mail: str) -> str:
        '''Takes a mail and returns a session id'''
        user = self._db._session.query(User).filter_by(email=mail).first()
        if user is not None:
            session_id = self._generate_uuid()
            user.session_id = session_id
            self._db._session.commit()
            return user.session_id
