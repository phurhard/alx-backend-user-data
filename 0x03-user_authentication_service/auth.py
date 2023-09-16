#!/usr/bin/env python3
'''Authentication'''
import bcrypt
from user import User
from db import DB
import uuid


def _generate_uuid() -> uuid:
    '''Generate a uuid'''
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        '''initialization'''
        self._db = DB()

    def _hash_password(self, pwd: str) -> bin:
        '''Takes a password string and returns a binary
        representation of the string'''
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
        '''Takes a mail and generates a session id,
        used at the start of a user loging in to the site'''
        user = self._db._session.query(User).filter_by(email=mail).first()
        if user is not None:
            session_id = self._generate_uuid()
            user.session_id = session_id
            self._db._session.commit()
            return user.session_id

    def get_user_from_session_id(self, sessionId: str) -> User:
        '''Takes a session id and returns the user'''
        user = self._db._session.query(User
                                       ).filter_by(
                                           session_id=sessionId).first()
        if user is not None:
            return user
        else:
            return None

    def destroy_session(self, userId: int) -> None:
        '''Destroys a session for a given user id'''
        user = self._db._session.query(User
                                       ).filter_by(id=userId).first()
        if user:
            user.session_id = None
        return None

    def get_reset_password_token(self, mail: str) -> str:
        '''Generates a password reset token for a given mail'''
        user = self._db._session.query(User).filter_by(email=mail).first()
        if user is None:
            raise ValueError
        else:
            token = _generate_uuid()
            user.reset_token = token
            return user.reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        '''Updates the password of the user which reset token was given'''
        user = self._db._session.query(User
                                       ).filter_by(
                                                   reset_token=reset_token
                                                   ).first()
        if user is None:
            raise ValueError
        else:
            user.reset_token = None
            newPwd = self._hash_password(password)
            user.hashed_password = newPwd
