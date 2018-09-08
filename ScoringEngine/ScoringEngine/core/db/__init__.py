"""
Copyright 2016 Brandon Warner

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ScoringEngine.core.conf import conf
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


_session = None

def getSession():
    global _session
    if _session is None:
        _session = Session()
    return _session

def closeSession():
    global _session
    if _session is not None:
        _session.close()
        _session = None