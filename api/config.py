## config.py

from os import environ

username = environ.get('DB_USERNAME')
password = environ.get('DB_PASSWORD')
db_name = environ.get('DB_NAME')

DATABASE_URI = f'postgres+psycopg2://{username}:{password}@localhost:5432/{db_name}'
