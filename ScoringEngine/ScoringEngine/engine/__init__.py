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
import random
import datetime
from ScoringEngine.db import Session
import ScoringEngine.db.tables as tables
from ScoringEngine.conf import conf

running = False
event = None

def start():
    print "start scoring"
    thread = threading.Thread(target=thread_start)
    thread.start()

def thread_start():
    while running:
        print "loop"
        score()
        i = random.randint(conf['engine']['min'],conf['engine']['max'])
        date = datetime.datetime.now()
        date += datetime.timedelta(seconds=i)
        print "sleeping for %i (%s)" % (i, date)
        threading._sleep(i)

def score():
    session = Session()
    event = None
    events = session.query(tables.Event).filter(tables.Event.current == True)
    if events.count() > 0:
        event = events[0].id
    for server in session.query(tables.TeamServer).all():
        print server
        print server.team.name
        if (server.server.enabled and server.team.enabled):
            for service in session.query(tables.Service).filter(tables.and_(tables.Service.serverid==server.server.id,tables.Service.enabled==True)):
                print service.type.tester
                m=__import__(service.type.tester)
                func = getattr(m, "test")
                threading.Thread(target=func, args=[server,service,event]).start()
    session.close()