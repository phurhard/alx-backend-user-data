#!/usr/bin/env python3
''' User authentication service'''
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    '''User model'''
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __repr__(self) -> str:
        """Representation of the string"""
        return '<User (id="%s", email="%s", hashed_password="%s",\
                    session_id="%s", reset_token="%s")>' % (
                        self.id, self.email,
                        self.hashed_password, self.session_id,
                        self.reset_token)
