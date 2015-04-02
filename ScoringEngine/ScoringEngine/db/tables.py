from sqlalchemy import *
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
        return "<Team(id='%i', name='%s', network='%s')>" % (id,name,network)

class Server(Base):
    __tablename__ = 'servers'

    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    ip_3 = Column(String(3))
    ip_4 = Column(String(3), nullable=False)
    enabled = Column(Boolean, nullable=False)

    def __repr__(self):
        return "<Server(id='%i',name='%s',ip='%s.%s',enabled='%s')>" % self.id, self.name, self.ip_3, self.ip_4, self.enabled

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
    server = relationship("Server", backref=backref('team', order_by=teamid))

    def getIP(self):
        return team.network.replace("{3}",self.server.ip_3).replace("{4}",self.server.ip_4)

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
    serviceid = Column(Integer, ForeignKey('services.id'))
    key = Column(String(50), nullable=False)
    value = Column(Text)

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
    