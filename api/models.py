#!python3.8
from uuid import uuid4, UUID

from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    
    pid = Column(Integer, primary_key=True)
    uuid = Column(String, default=uuid4())
    username = Column(String, nullable=True)
    name = Column(String, nullable=True)
    email = Column(String)
    sms = Column(String, nullable=True)
    created = Column(Date, default=datetime.now())
    lastseen = Column(Date, default=datetime.now())

    def __repr__(self):
        return f"<User(username={self.username}, name={self.name}, email={self.email}, last seen={self.lastseen})>"
