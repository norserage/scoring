import threading
import random
from ScoringEngine.db import Session
import ScoringEngine.db.tables as tables

running = False

def start():
    print "start scoring"
    thread = threading.Thread(target=thread_start)
    thread.start()

def thread_start():
    while running:
        print "loop"
        score()
        i = random.randint(120,240)
        print "sleeping for %i" % (i)
        threading._sleep(i)

def score():
    session = Session()
    for server in session.query(tables.TeamServer).all():
        print server
        if (server.server.enabled):
            for service in session.query(tables.Service).filter(tables.and_(tables.Service.serverid==server.server.id,tables.Service.enabled==True)):
                print service.type.tester
                m=__import__(service.type.tester)
                func = getattr(m, "test")
                threading.Thread(target=func, args=[server,service]).start()