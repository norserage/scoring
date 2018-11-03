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
from sqlalchemy.sql import expression
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

    @staticmethod
    def current_event():
        from ScoringEngine.core.db import getSession
        return getSession().query(Event).filter(Event.current == True).first()
    
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

    id = Column(BigInteger, primary_key=True, index=True, unique=True, autoincrement=True)
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

    ###########
    # Columns #
    ###########
    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    name = Column(String(45))
    username = Column(String(25), nullable=False, unique=True, index=True)
    password = Column(String(60), nullable=False)
    team = Column(Integer, nullable=False)
    group = Column(Integer, nullable=False)

    ###########################
    # Helpers for flask_login #
    ###########################
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    ####################
    # Password Helpers #
    ####################
    def set_password(self, new_password):
        import bcrypt
        self.password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

    def verify_password(self, password):
        import bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

    #####################
    # Helper Properties #
    #####################
    @property
    def team_name(self):
        if self.team != -1:
            from ScoringEngine.core.db import Session
            session = Session()
            team = session.query(Team).filter(Team.id==self.team)
            if team.count() > 0:
                return team[0].name
        return "No Team"

    @property
    def group_name(self):
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

    @property
    def settings(self):
        return dict([(s.key, s.value) for s in self.db_settings])

    ##################
    # Static Helpers #
    ##################
    @staticmethod
    def create(name, username, new_password, team, group):
        u = User()
        u.name = name
        u.username = username
        u.team = team
        u.group = group
        u.set_password(new_password)
        return u

    ####################
    # Helper Functions #
    ####################
    def set_user_setting(self, setting, value):
        from ScoringEngine.core.db import getSession
        s = getSession().query(UserSetting).filter(UserSetting.userid == self.id and UserSetting.key == setting).first()
        if not s:
            s = UserSetting()
            s.userid = self.id
            s.key = setting
            getSession().add(s)
        s.value = value


class UserSetting(Base):
    __tablename__ = 'usersettings'

    userid = Column(Integer, ForeignKey('users.id'), primary_key=True, index=True, autoincrement=False)
    key = Column(String(30), primary_key=True, index=True)
    value = Column(String(100))

    user = relationship("User", backref=backref('db_settings'))

class Log(Base):
    __tablename__ = 'log'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    time = Column(DateTime, nullable=False)
    severity = Column(Integer, nullable=False)
    module = Column(String(60), nullable=False)
    message = Column(Text, nullable=False)

class IncedentResponse(Base):
    __tablename__ = 'incedentresponses'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    eventid = Column(Integer, ForeignKey('events.id'), index=True, unique=False)
    teamserverid = Column(Integer, ForeignKey('teamservers.id'), index=True, unique=False)
    addedby = Column(Integer, ForeignKey('users.id'), unique=False, index=False)
    added = Column(DateTime, nullable=False)
    points = Column(Integer, nullable=False)
    comments = Column(Text,nullable=False)



class IncedentResponseAttachment(Base):
    __tablename__ = 'incedentresponseattachments'

    id = Column(Integer, primary_key=True, index=True, unique=True)
    irid = Column(Integer, ForeignKey('incedentresponses.id'))
    filename = Column(String(255), nullable=False)
    data = Column(LargeBinary, nullable=False)
    size = Column(Integer, nullable=False)
    added_by = Column(Integer, ForeignKey("users.id"))
    added = Column(DateTime, nullable=False)

    ir = relationship("IncedentResponse", backref=backref('files', order_by=id))




class InjectCategory(Base):
    __tablename__ = 'injectcategories'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    parentid = Column(Integer, nullable=True, index=True)
    name = Column(String(255), nullable=False)

    @property
    def children(self):
        from ScoringEngine.core.db import getSession
        return getSession().query(InjectCategory).filter(InjectCategory.parentid == self.id)

    


class Inject(Base):
    __tablename__ = 'injects'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    categoryid = Column(Integer, ForeignKey('injectcategories.id'))
    subject = Column(String(255), nullable=False)
    body = Column(Text, nullable=False)
    duration = Column(Integer, nullable=False)
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

    @property
    def should_show(self):
        from datetime import datetime, timedelta
        if self.event.current and datetime.utcnow() >= self.when and (datetime.utcnow() <= (self.when + timedelta(minutes=self.duration)) or self.allowlate):
            return True
        return False

    @property
    def end(self):
        from datetime import timedelta
        return self.when + timedelta(minutes=self.duration)

    @property
    def due_in(self):
        from datetime import datetime
        return self.end - datetime.utcnow()

    inject = relationship("Inject")
    event = relationship("Event", backref=backref('injects', order_by=when))

class TeamInjectSubmission(Base):
    __tablename__ = 'teaminjectsubmissions'

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    assignedinjectid = Column(Integer, ForeignKey("assignedinjects.id"))
    teamid = Column(Integer, ForeignKey("teams.id"))
    when = Column(DateTime, nullable=False)
    body = Column(Text, nullable=False)
    points = Column(Integer, nullable=False)

    inject = relationship("AssignedInject", backref=backref('submissions'))
    team = relationship("Team")

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
    data = Column(LargeBinary, nullable=False)

    inject = relationship("TeamInjectSubmission", backref=backref('files'))
