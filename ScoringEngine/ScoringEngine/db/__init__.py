from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ScoringEngine.conf import conf
import tables
import pprint
import Crypto.Hash.MD5
#engine = create_engine('mysql://scoring:scoring@10.151.9.10/scoring')

pprint.pprint(conf)
engine = create_engine(conf['database'])
Session = sessionmaker(bind=engine)

def createUser(name,username,password,team,group):
    session = Session()
    user = tables.User()
    user.name = name
    user.username = username
    m = Crypto.Hash.MD5.new()
    m.update(password)
    user.password = m.hexdigest()
    user.team = team
    user.group = group
    session.add(user)
    session.commit()
    session.close()
