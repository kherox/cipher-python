from sqlalchemy import Column, Integer, String , DateTime , text , Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class HashTable(Base):
    __tablename__ = "hasher_data_table"

    hash_id = Column(Integer, primary_key=True)
    hash_key = Column(String(350), nullable=False)
    hash_data_value = Column(String(350), nullable=False)
    hash_created_date = Column(DateTime, server_default=text('NOW()'))


    def __repr__(self):
        return "Hash ID : " + self.hash_id  + " Hash Data : " + self.hash_data_value

class KeyTable(Base):
    __tablename__ = "key_table"

    key_id = Column(Integer,primary_key=True)
    key_value = Column(String(350) , nullable=False)
    key_status = Column(Boolean)
    key_update_date = Column(DateTime , nullable=True)
    key_created_date = Column(DateTime ,server_default=text('NOW()'))