from sqlalchemy import *
from sqlalchemy.sql import exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
metadata = MetaData()
Base = declarative_base()

class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    network = Column(String(15), nullable=False)
    enabled = Column(Boolean, nullable=False)

    def __repr__(self):
        return "<Team(id='%i', name='%s', network='%s')>" % (self.id,self.name,self.network)

class Server(Base):
    __tablename__ = 'servers'

    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    ip_3 = Column(String(3))
    ip_4 = Column(String(3), nullable=False)
    enabled = Column(Boolean, nullable=False)

    def __repr__(self):
        return "<Server(id='%i',name='%s',ip='%s.%s',enabled='%s')>" % (self.id, self.name, self.ip_3, self.ip_4, self.enabled)

class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True)
    serverid = Column(Integer, ForeignKey('servers.id'))
    name = Column(String(25), nullable=False)
    port = Column(Integer)
    typeid = Column(Integer, ForeignKey('servicetypes.id'))
    enabled = Column(Boolean, nullable=False)

    server = relationship("Server", backref=backref('services', order_by=id))
    type = relationship("ServiceType", backref=backref('services', order_by=id))

    def __repr__(self):
        pass

class ServiceType(Base):
    __tablename__ = 'servicetypes'

    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    tester = Column(String(25), nullable=False)

class TeamServer(Base):
    __tablename__ = 'teamservers'
    
    id = Column(Integer, primary_key=True)
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

    id = Column(Integer, primary_key=True)
    teamserverid = Column(Integer, ForeignKey('teamservers.id'))
    serviceid = Column(Integer, ForeignKey('services.id'))
    scoretime = Column(DateTime, nullable=False)
    up = Column(Boolean, nullable=False)
    info = Column(Text)

    teamserver = relationship("TeamServer", backref=backref('scores', order_by=scoretime))
    service = relationship("Service", backref=backref('scores', order_by=teamserverid))

class ServiceArg(Base):
    __tablename__ = 'serviceargs'

    id = Column(Integer, primary_key=True)
    serverid = Column(Integer, ForeignKey('teamservers.id'))
    serviceid = Column(Integer, ForeignKey('services.id'))
    key = Column(String(50), nullable=False)
    value = Column(Text)

    teamserver = relationship("TeamServer", backref=backref('serviceargs', order_by=id))
    service = relationship("Service", backref=backref('args', order_by=id))


class PasswordDatabase(Base):
    __tablename__ = 'passdb'

    id = Column(Integer, primary_key=True)
    db = Column(String(10), nullable=False)
    domain = Column(String(15))
    user = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255))

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(45))
    username = Column(String(25), nullable=False)
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
            return "2"
        elif self.group == 3:
            return "Judge"
        elif self.group == 4:
            return "Manager"
        elif self.group == 5:
            return "Admin"

class Log(Base):
    __tablename__ = 'log'

    id = Column(Integer, primary_key=True)
    time = Column(DateTime, nullable=False)
    severity = Column(Integer, nullable=False)
    module = Column(String(60), nullable=False)
    message = Column(Text, nullable=False)

class InjectCategory(Base):
    __tablename__ = 'injectcategories'

    id = Column(Integer, primary_key=True)
    parentid = Column(Integer)
    name = Column(String(255), nullable=False)


class Inject(Base):
    __tablename__ = 'injects'

    id = Column(Integer, primary_key=True)
    categoryid = Column(Integer, ForeignKey('injectcategories.id'))
    subjet = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    durration = Column(Integer, nullable=False)


    category = relationship("InjectCategory", backref=backref('injects', order_by=id))

class AssignedInject(Base):
    __tablename__ = 'assignedinjects'

    id = Column(Integer, primary_key=True)
    injectid = Column(Integer, ForeignKey('injects.id'))
    subject = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    when = Column(DateTime, nullable=False)
    duration = Column(Integer, nullable=False)
    allowlate = Column(Boolean, nullable=False)

    inject = relationship("Inject")

class TeamInjectSubmission(Base):
    __tablename__ = 'teaminjectsubmissions'

    id = Column(Integer, primary_key=True)
    assignedinjectid = Column(Integer, ForeignKey("assignedinjects.id"))
    teamid = Column(Integer, ForeignKey("teams.id"))
    when = Column(DateTime, nullable=False)
    body = Column(Text, nullable=False)

    teamserver = relationship("TeamServer", backref=backref('serviceargs', order_by=id))

class TeamInjectSubmissionNote(Base):
    __tablename__ = 'teaminjectsubmissionnotes'

    id = Column(Integer, primary_key=True)
    teaminjectid = Column(Integer, ForeignKey("teaminjectsubmissions.id"))
    userid = Column(Integer, ForeignKey("users.id"))
    visible = Column(Boolean, nullable=False)


class TeamInjectSubmissionAttachment(Base):
    __tablename__ = 'teaminjectsubmissionattachments'

    id = Column(Integer, primary_key=True)
    teaminjectid = Column(Inject, ForeignKey("teaminjectsubmissions.id"))
    filename = Column(String(255), nullable=False)
    size = Column(Integer, nullable=False)
    #data = Column(BLOB, nullable=False) Blobs suck in pgsql so we will store as file on file system or in a nosql document store