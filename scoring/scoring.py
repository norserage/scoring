from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import threading
import tables
import random
from json import *

# Note we did not loose the bug
'''
       / .'
 .---. \/
(._.' \()
 ^"""^"
bug
'''


class ScoringEngine:
    
    def __init__(self):
        #self.loadConfig("settings.json")
        self.engine = create_engine('mysql://scoring:scoring@10.151.9.10/scoring')
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.scoring = Scoring(self.session)
        self.running = False

    def loadConfig(self, file):
        conf_fp = open(file)
        self.config = load(conf_fp)
        conf_fp.close()

    def startScoring(self):
        self.thread = threading.Thread(target=self.threadScoring)
        self.thread.start()

    def threadScoring(self):
        while self.running:
            self.scoring.score()
            threading._sleep(random.randint(120,240))

class Scoring:
    def __init__(self, session):
        self.session = session
    def score(self):
        for server in self.session.query(tables.TeamServer):
            if (server.server.enabled):
                for service in server.services:
                    m=__import__(service.type.tester)
                    func = getattr(m, "test")
                    threading.Thread(target=func, args=[server,service,self.session]).start()

if __name__ == "main":
    se = ScoringEngine();