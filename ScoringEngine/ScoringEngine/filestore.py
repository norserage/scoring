__author__ = 'thebmw'
import bsddb3.db
import uuid
from ScoringEngine.conf import conf
db = None
def init():
    db = bsddb3.db.DB()
    db.open(conf['filedb'])

def insert(data):
    id = uuid.uuid4()
    db.put(id, data)
    return id

def get(id):
    return db.get(id)

def butts():
    print("butts")
    return


