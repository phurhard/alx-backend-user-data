#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
# from sqlalchemy.exc import InvalidRequestError
# from sqlalchemy.exc import NotFoundError
from typing import List

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str,
                 hashed_password: str) -> User:
        '''Creates a new user n adds to the db'''
        session = self._session
        newUser = User()
        newUser.email = email
        newUser.hashed_password = hashed_password
        session.add(newUser)
        session.commit()
        return newUser

    def find_user_by(param: str) -> List:
        '''Finds the first occurence of a user'''
        session = self._session
        user = session.query(User).filter(param).first()
        return user
