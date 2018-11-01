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
from ScoringEngine.core.db import Session, tables
from ScoringEngine.core import config, logger


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
    session = Session()
    event = None
    events = session.query(tables.Event).filter(tables.Event.current == True)
    if events.count() > 0:
        event = events[0].id
        logger.info("Score Event: %i" % events[0].name)
    for server in session.query(tables.TeamServer).all():
        if server.server.enabled and server.team.enabled:
            for service in session.query(tables.Service).filter(
                    tables.and_(tables.Service.serverid == server.server.id, tables.Service.enabled == True)):
                m = __import__(service.type.tester)
                func = getattr(m, "test")
                logger.debug("Score: %s(<%s>, <%s>, <%s>, <%s>)" % (service.type.tester, server.team.name, server.server.name, service.name, event))
                threading.Thread(target=func, args=[server, service, event]).start()
    session.close()
