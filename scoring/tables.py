from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
metadata = MetaData()
Base = declarative_base()

class Team(Base):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    network = Column(String(15), nullable=False)

    def __repr__(self):
        return "<Team(id='%i', name='%s', network='%s')>" % (id,name,network)

class Server(Base):
    __tablename__ = 'servers'

    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False)
    ip_3 = Column(String(3))
    ip_4 = Column(String(3), nullable=False)
    enabled = Column(Boolean, nullable=False)



team = Table('teams', metadata,
             Column('id', Integer, primary_key=True),
             Column('name', String(25), nullable=False),
             Column('network', String(15), nullable=False),
)

server = Table('servers', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String(25), nullable=False),
              Column('ip_3', String(3)),
              Column('ip_4', String(3), nullable=False),
              Column('enabled', Boolean, nullable=False),
)

service = Table('services', metadata,
              Column('id', Integer, primary_key=True),
              Column('serverid', Integer, ForeignKey('servers.id')),
              Column('name', String(25), nullable=False),
              Column('port', Integer),
              Column('typeid', Integer, ForeignKey('servicetypes.id')),
              Column('enabled', Boolean, nullable=False),
)

servicetype = Table('servicetypes', metadata,
              Column('id', Integer, primary_key=True),
              Column('name', String(25), nullable=False),
              Column('tester', String(25), nullable=False)
)

teamserver = Table('teamservers', metadata,
              Column('id', Integer, primary_key=True),
              Column('teamid', Integer, ForeignKey('teams.id')),
              Column('serverid', Integer, ForeignKey('servers.id')),
)

scoreevent = Table('scoreevents', metadata,
              Column('id', Integer, primary_key=True),
              Column('teamserverid', Integer, ForeignKey('teamservers.id')),
              Column('serviceid', Integer, ForeignKey('services.id')),
              Column('scoretime', DateTime, nullable=False),
              Column('up', Boolean, nullable=False),       
)

servicearg = Table('serviceargs', metadata,
              Column('id', Integer, primary_key=True),
              Column('serviceid', Integer, ForeignKey('services.id')),
              Column('key', String(50), nullable=False),
              Column('value', Text),
)