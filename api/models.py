#!python3.8
from uuid import uuid4

class User:

    def __init__(self):
        self.uid = uuid4()

users = {}