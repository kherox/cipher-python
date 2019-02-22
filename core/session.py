from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .model import Base

engine = create_engine("mysql+pymysql://hasher:password@192.168.1.141/hasher_data")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


