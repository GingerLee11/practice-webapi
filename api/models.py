#!python3.8
from uuid import uuid4

from datetime import datetime
import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Date, UniqueConstraint
from sqlalchemy.orm import sessionmaker

import smtplib, ssl

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    
    pid = Column(Integer, primary_key=True)
    uuid = Column(String, default=str(uuid4()).replace('-', ''))
    username = Column(String, nullable=True)
    name = Column(String, nullable=True)
    email = Column(String, unique=True)
    password = Column(String)
    sms = Column(String, nullable=True)
    created = Column(Date, default=datetime.now())
    lastseen = Column(Date, default=datetime.now())

    __table_args__ = (UniqueConstraint('uuid', 'email'),)

    def __repr__(self):
        return f"<User(uuid={self.uuid}, username={self.username}, name={self.name}, email={self.email}, last seen={self.lastseen})>"


class Token(Base):
    __tablename__ = 'tokens'

    pid = Column(Integer, primary_key=True)
    email = Column(String)
    uuid = Column(String, default=str(uuid4()).replace('-', ''))

    def __repr__(self):
        return f"<User(uuid={self.uuid}, username={self.email})>"
    


## config.py
from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = os.environ.get('DATABASE_URI')


smtp_server = os.environ.get('SMTP_SERVER')
port = os.environ.get('PORT')
send_email = os.environ.get('SENDER_EMAIL')
email_password = os.environ.get('SENDER_EMAIL_PASSWORD') 

def send_python_email(receiver_email, message):
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(send_email, email_password)
        server.sendmail(send_email, receiver_email, message)
    """
    with smtplib.SMTP(host=host, port=port) as server:
        server.starttls(context=context)
        server.login(send_email, email_password)
        server.sendmail(send_email, receiver_email, message)
    """
## crud.py

engine = create_engine(DATABASE_URI)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    recreate_database()
