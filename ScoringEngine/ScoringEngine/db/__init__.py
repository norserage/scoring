from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ScoringEngine.conf import conf
import tables
import pprint
#engine = create_engine('mysql://scoring:scoring@10.151.9.10/scoring')

pprint.pprint(conf)
engine = create_engine(conf['database'])
Session = sessionmaker(bind=engine)

def createUser(name,username,password,team,group):
    session = Session()
    user = tables.User()
