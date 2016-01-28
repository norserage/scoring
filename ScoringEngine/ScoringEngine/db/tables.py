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
from sqlalchemy import *
from ScoringEngine.db.customTypes import *
from sqlalchemy.sql import exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
metadata = MetaData()
Base = declarative_base()

def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    current = Column(Boolean, index=True, unique=False)
    start = Column(DateTime, index=True, unique=False)
    end = Column(DateTime, index=True, unique=False)

    def seralize(self):
        return {
            'id':self.id,
            'name':self.name,
            'current': self.current,
            'start':dump_datetime(self.start),
            'end':dump_datetime(self.end)
            }
    
class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String(25), nullable=False)
    network = Column(String(15), nullable=False)
    enabled = Column(Boolean, nullable=False)

    def __repr__(self):
        return "<Team(id='%i', name='%s', network='%s')>" % (self.id, self.name, self.network)

class Server(Base):
    __tablename__ = 'servers'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String(25), nullable=False)
    enabled = Column(Boolean, nullable=False)
    ip_3 = Column(String(3))
    ip_4 = Column(String(3), nullable=False)

    def __repr__(self):
        return "<Server(id='%i',name='%s',ip='%s.%s')>" % (self.id, self.name, self.ip_3, self.ip_4, self.enabled)

class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    serverid = Column(Integer, ForeignKey('servers.id'))
    enabled = Column(Boolean, nullable=False)
    name = Column(String(25), nullable=False)
    port = Column(Integer)
    typeid = Column(Integer, ForeignKey('servicetypes.id'))

    server = relationship("Server", backref=backref('services', order_by=id))
    type = relationship("ServiceType", backref=backref('services', order_by=id))

    def __repr__(self):
        pass

    def arg(self, name):
        return (arg.value for arg in self.args if arg.key == name)


class ServiceType(Base):
    __tablename__ = 'servicetypes'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String(25), nullable=False)
    tester = Column(String(25), nullable=False)

class TeamServer(Base):
    __tablename__ = 'teamservers'
    
    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    teamid = Column(Integer, ForeignKey('teams.id'))
    serverid = Column(Integer, ForeignKey('servers.id'))

    team = relationship("Team", backref=backref('servers', order_by=serverid))
    server = relationship("Server", backref=backref('teams', order_by=teamid))

    def getIP(self):
        if self.server.ip_3 == None:
            return self.team.network.replace("{4}",self.server.ip_4)
        else:
            return self.team.network.replace("{3}",self.server.ip_3).replace("{4}",self.server.ip_4)

class ScoreEvent(Base):
    __tablename__ = 'scoreevents'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    eventid = Column(Integer, ForeignKey('events.id'), index=True, unique=False)
    teamserverid = Column(Integer, ForeignKey('teamservers.id'), index=True, unique=False)
    serviceid = Column(Integer, ForeignKey('services.id'), index=True, unique=False)
    scoretime = Column(DateTime, nullable=False, index=True, unique=False)
    up = Column(Boolean, nullable=False)
    info = Column(Text)

    teamserver = relationship("TeamServer", backref=backref('scores', order_by=scoretime))
    service = relationship("Service", backref=backref('scores', order_by=teamserverid))

class ServiceArg(Base):
    __tablename__ = 'serviceargs'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    serverid = Column(Integer, ForeignKey('teamservers.id'))
    serviceid = Column(Integer, ForeignKey('services.id'))
    key = Column(String(50), nullable=False)
    value = Column(Text)

    teamserver = relationship("TeamServer", backref=backref('serviceargs', order_by=id))
    service = relationship("Service", backref=backref('args', order_by=id))


class PasswordDatabase(Base):
    __tablename__ = 'passdb'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String(25), nullable=False, index=True, unique=True)
    domain = Column(String(15))

class PasswordDatabaseEntry(Base):
    __tablename__ = 'passdbentry'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    passdbid = Column(Integer, ForeignKey('passdb.id'), index=True)
    user = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255))

    passdb = relationship("PasswordDatabase", backref=backref('entries', order_by=id))

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String(45))
    username = Column(String(25), nullable=False, unique=True, index=True)
    password = Column(String(60), nullable=False)
    team = Column(Integer, nullable=False)
    group = Column(Integer, nullable=False)

    def getTeam(self):
        if self.team != -1:
            from ScoringEngine.db import Session
            session = Session()
            team = session.query(Team).filter(Team.id==self.team)
            if team.count() > 0:
                return team[0].name
        return "No Team"

    def getGroupName(self):
        if self.group == 1:
            return "User"
        elif self.group == 2:
            return "Room Judge"
        elif self.group == 3:
            return "Judge"
        elif self.group == 4:
            return "Manager"
        elif self.group == 5:
            return "Admin"

class Log(Base):
    __tablename__ = 'log'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    time = Column(DateTime, nullable=False)
    severity = Column(Integer, nullable=False)
    module = Column(String(60), nullable=False)
    message = Column(Text, nullable=False)

class InjectCategory(Base):
    __tablename__ = 'injectcategories'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    parentid = Column(Integer)
    name = Column(String(255), nullable=False)

    


class Inject(Base):
    __tablename__ = 'injects'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    categoryid = Column(Integer, ForeignKey('injectcategories.id'))
    subjet = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    durration = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False)


    category = relationship("InjectCategory", backref=backref('injects', order_by=id))

class AssignedInject(Base):
    __tablename__ = 'assignedinjects'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    eventid = Column(Integer, ForeignKey('events.id'))
    injectid = Column(Integer, ForeignKey('injects.id'))
    subject = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    when = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)
    allowlate = Column(Boolean, nullable=False)
    points = Column(Integer, nullable=False)

    inject = relationship("Inject")

class TeamInjectSubmission(Base):
    __tablename__ = 'teaminjectsubmissions'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    assignedinjectid = Column(Integer, ForeignKey("assignedinjects.id"))
    teamid = Column(Integer, ForeignKey("teams.id"))
    when = Column(DateTime, nullable=False)
    body = Column(Text, nullable=False)
    points = Column(Integer, nullable=False)

    inject = relationship("AssignedInject", backref=backref('submissions', order_by=id))

class TeamInjectSubmissionNote(Base):
    __tablename__ = 'teaminjectsubmissionnotes'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    teaminjectid = Column(Integer, ForeignKey("teaminjectsubmissions.id"))
    userid = Column(Integer, ForeignKey("users.id"))
    visible = Column(Boolean, nullable=False)


class TeamInjectSubmissionAttachment(Base):
    __tablename__ = 'teaminjectsubmissionattachments'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    teaminjectid = Column(Integer, ForeignKey("teaminjectsubmissions.id"))
    filename = Column(String(255), nullable=False)
    size = Column(Integer, nullable=False)
    #fileid = Column(UUID, nullable=False)
    #data = Column(BLOB, nullable=False) Blobs suck in pgsql so we will store as file on file system or in a nosql document store