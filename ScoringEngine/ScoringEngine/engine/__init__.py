import threading
import random
import datetime
from ScoringEngine.db import Session
import ScoringEngine.db.tables as tables

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
        i = random.randint(60,240)
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
        if (server.server.enabled):
            for service in session.query(tables.Service).filter(tables.and_(tables.Service.serverid==server.server.id,tables.Service.enabled==True)):
                print service.type.tester
                m=__import__(service.type.tester)
                func = getattr(m, "test")
                threading.Thread(target=func, args=[server,service,event]).start()
    session.close()