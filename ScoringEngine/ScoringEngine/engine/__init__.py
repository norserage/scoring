﻿"""
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
import threading
import time
import random
import datetime
import json
from ScoringEngine.core.db import Session, tables
from ScoringEngine.core import config, logger


class EngineHelperCommon:
    def get_engine_services(self, engine_id):
        raise NotImplementedError()

    def save_new_service_status(self, team_server_id, service_id, event, status, extra_info):
        raise NotImplementedError()

    def get_current_event(self):
        raise NotImplementedError()

    def get_random_user(self, password_database):
        raise NotImplementedError()


class APIEngineHelper(EngineHelperCommon):
    pass


class DBEngineHelper(EngineHelperCommon):

    def get_current_event(self):
        session = Session()
        event = session.query(tables.Event).filter(tables.Event.current == True).first()
        session.close()
        if event:
            return event.seralize()
        else:
            return None

    def get_engine_services(self, engine_id):
        session = Session()
        services = []
        engine = session.query(tables.Engine).filter(tables.Engine.id == engine_id).first()
        if engine:
            engine.last_checkin = datetime.datetime.utcnow()
        session.commit()
        for server in session.query(tables.TeamServer).filter(tables.Team.enabled == True and tables.Server.enabled == True):
            for service in session.query(tables.Service).filter(tables.Service.serverid == server.server.id and tables.Service.enabled == True):
                s = {}
                s['test'] = service.type.tester
                s['ip'] = server.getIP()
                s['server_name'] = server.server.name
                s['port'] = service.port
                s['service'] = service.id
                s['service_name'] = service.name
                s['team'] = server.team.id
                s['team_name'] = server.team.name
                services.append(s)
        session.close()
        return services

    def get_random_user(self, password_database):
        session = Session()
        user = []
        passwddb = session.query(tables.PasswordDatabase).filter(tables.PasswordDatabase.name == password_database).first()
        for usr in passwddb.entries:
            user.append({'user': usr.user, 'pass': usr.password, 'domain': usr.passdb.domain, 'email': usr.email})
        outuser = random.choice(user)
        session.close()
        return outuser

    def save_new_service_status(self, team_server_id, service_id, event, status, extra_info):
        session = Session()
        se = tables.ScoreEvent()
        se.engineid = config.get_item("engine/id")
        se.eventid = event['id']
        se.teamserverid = team_server_id
        se.serviceid = service_id
        se.up = status
        se.info = json.dumps(extra_info)
        session.close()


helper = EngineHelperCommon()

def setup_helper(db=False):
    global helper
    if db:
        helper = DBEngineHelper()
    else:
        helper = APIEngineHelper()

def thread_start():
    while True:
        logger.info("Score Loop Starting")
        score()
        i = random.randint(config.get_item("engine/min"), config.get_item("engine/max"))
        date = datetime.datetime.now()
        date += datetime.timedelta(seconds=i)
        logger.debug("Score Loop sleeping for %i (%s)" % (i, date))
        time.sleep(i)


def score():
    # session = Session()
    # engine = session.query(tables.Engine).filter(tables.Engine.id == config.get_item("engine/id")).first()
    # if engine:
    #     engine.last_checkin = datetime.datetime.now()
    event = helper.get_current_event()
    services = helper.get_engine_services(config.get_item("engine/id"))

    for service in services:
        m = __import__(service['test'])
        func = getattr(m, "test")
        logger.debug("Score: %s(<%s>, <%s>, <%s>, <%s>)" % (service['test'], service['ip'], service['port'], service['service_name'], event['name'] if 'name' in event else None))
        threading.Thread(target=func, args=[event, service])

    # for server in session.query(tables.TeamServer).all():
    #     if server.server.enabled and server.team.enabled:
    #         for service in session.query(tables.Service).filter(
    #                 tables.and_(tables.Service.serverid == server.server.id, tables.Service.enabled == True)):
    #             m = __import__(service.type.tester)
    #             func = getattr(m, "test")
    #             logger.debug("Score: %s(<%s>, <%s>, <%s>, <%s>)" % (service.type.tester, server.team.name, server.server.name, service.name, event))
    #             threading.Thread(target=func, args=[server, service, event]).start()
    # session.close()


