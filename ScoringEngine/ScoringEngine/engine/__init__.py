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

    def save_new_service_status(self, event, service, status, extra_info):
        raise NotImplementedError()

    def get_current_event(self):
        raise NotImplementedError()

    def get_random_user(self, password_database):
        raise NotImplementedError()

    def get_service_config_old(self, team_server_id, service_id):
        raise NotImplementedError()


class APIEngineHelper(EngineHelperCommon):
    def __init__(self):
        import requests
        self.req = requests
        self.headers = {
            'Authorization': "Bearer %s" % config.get_item("engine/psk"),
            'X-ENGINE-ID': str(config.get_item("engine/id"))
        }

    def _build_url(self, path):
        return "%s/%s" % (config.get_item("engine/api_url"), path)

    def _get(self, url):
        return self.req.get(url, headers=self.headers)

    def _post(self, url, data):
        return self.req.post(url, json=data, headers=self.headers)

    def get_current_event(self):
        return self._get(self._build_url("event/current")).json()

    def get_random_user(self, password_database):
        return self._get(self._build_url("password_db/%s/user/random" % password_database)).json()

    def get_engine_services(self, engine_id):
        return self._get(self._build_url("engine/%d/services" % engine_id)).json()

    def get_service_config_old(self, team_server_id, service_id):
        return self._get(self._build_url("teamserver/%s/service/%s/config_legacy" % (team_server_id, service_id))).json()

    def save_new_service_status(self, event, service, status, extra_info):
        self._post(self._build_url("event/%s/teamserver/%s/service/%s/status" % (event['id'], service['team_server_id'], service['service_id'])), {
            "status": status,
            "info": extra_info
        })


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
        for server in session.query(tables.TeamServer).filter(tables.and_(tables.Team.enabled == True, tables.Server.enabled == True, tables.TeamServer.engine_id == engine_id)):
            for service in session.query(tables.Service).filter(tables.and_(tables.Service.serverid == server.server.id,tables.Service.enabled == True)):
                s = {}
                s['test'] = service.type.tester
                s['ip'] = server.getIP()
                s['server_name'] = server.server.name
                s['port'] = service.port
                s['service_id'] = service.id
                s['service_name'] = service.name
                s['team_id'] = server.team.id
                s['team_name'] = server.team.name
                s['team_server_id'] = server.id
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

    def save_new_service_status(self, event, service, status, extra_info, engine=None):
        session = Session()
        se = tables.ScoreEvent()
        se.engineid = config.get_item("engine/id") if engine is None else engine
        se.eventid = event['id'] if event is not None else None
        se.teamserverid = service['team_server_id']
        se.serviceid = service['service_id']
        se.scoretime = datetime.datetime.utcnow()
        se.up = status
        se.info = json.dumps(extra_info)
        session.add(se)
        session.commit()
        session.close()

    def get_service_config_old(self, team_server_id, service_id):
        session = Session()
        confpair = session.query(tables.ServiceArg).filter(
            tables.and_(tables.ServiceArg.serviceid == service_id, tables.ServiceArg.key == 'conf',
                        tables.ServiceArg.serverid == team_server_id))
        session.close()
        if confpair.count() > 0:
            conf = json.loads(confpair[0].value)
            return conf
        else:
            return {}


helper = EngineHelperCommon()

def setup_helper(db=False):
    global helper
    if db:
        helper = DBEngineHelper()
    else:
        helper = APIEngineHelper()

def set_helper(new_helper):
    global helper
    print(helper)
    if new_helper is not None:
        helper = new_helper
    print(helper)

def get_helper():
    return helper

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
    if event is not None:
        logger.debug("Event: '%s' Round: %d" % (event['name'], event['round']))
    services = helper.get_engine_services(config.get_item("engine/id"))

    for service in services:
        m = __import__(service['test'])
        func = getattr(m, "test")
        logger.debug("Score: %s(<%s>, <%s>, <%s>, <%s>)" % (service['test'], service['ip'], service['port'], service['service_name'], event['name'] if event is not None and 'name' in event else None))
        threading.Thread(target=func, args=[event, service]).start()

    # for server in session.query(tables.TeamServer).all():
    #     if server.server.enabled and server.team.enabled:
    #         for service in session.query(tables.Service).filter(
    #                 tables.and_(tables.Service.serverid == server.server.id, tables.Service.enabled == True)):
    #             m = __import__(service.type.tester)
    #             func = getattr(m, "test")
    #             logger.debug("Score: %s(<%s>, <%s>, <%s>, <%s>)" % (service.type.tester, server.team.name, server.server.name, service.name, event))
    #             threading.Thread(target=func, args=[server, service, event]).start()
    # session.close()


