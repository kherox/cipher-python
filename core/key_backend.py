from cryptography.fernet import Fernet
import redis
import hashlib


#from sqlalchemy import  DateTime 

import datetime

from model import HashTable , KeyTable
from session import Session

client = redis.Redis()

#client.flushall()
#client.flushdb()

class KeyBackend(object):

    def __init__(self):
        self.session = Session()
        if client.get("key") is None :
            self._key = Fernet.generate_key()
            client.delete("key")
            client.set("key",self._key)
            self.storeKey(self._key)
        else :
            self._key = client.get("key")
        self._fernet = Fernet(self._key)
        self.sha256 = hashlib.sha256()
    
    def storeHash(self,hash,key):
        data = HashTable(hash_key=key , hash_data_value=hash)
        self.session.add(data) 
        self.session.commit()

    def receiveHashKey(self,hash):
        query = self.session.query(HashTable).filter(HashTable.hash_data_value==hash).first()
        return query
    
    def storeKey(self,key):
        self.updateKeyStatus()
        k = KeyTable(key_value=key , key_status=True)
        self.session.add(k)
        self.session.commit()

    def receiveKey(self,key):
        query = self.session.query(KeyTable).filter(KeyTable.key_value==key , KeyTable.key_status==True).first()
        return query
    
    def updateKeyStatus(self):
        kTable = self.session.query(KeyTable).filter(KeyTable.key_status==True).first()
        if kTable is not None :
            kTable.key_status = False
            kTable.key_update_date = datetime.datetime.now()
            self.session.add(kTable)
            self.session.commit()
            return True 
        return False
    
    @property
    def fernet(self):
        return self._fernet
    
    @fernet.setter 
    def fernet(self , fernet) :
        self._fernet = fernet

    @property
    def key(self):
        return self._key
    
    
    def keys(self , key):
        self._key = key 
        self._fernet = Fernet(key)
