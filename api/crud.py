from sqlalchemy import create_engine

from api.config import DATABASE_URI
from api.models import Base

engine = create_engine(DATABASE_URI)

def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)