﻿import ScoringEngine.db.tables as tables
from ScoringEngine.db import Session
import json
import ScoringEngine.utils
import subprocess
import random
from datetime import datetime

def test(server, service, event):
    session = Session()
    se = tables.ScoreEvent()
    se.serviceid = service.id;
    se.teamserverid = server.id;
    se.scoretime = datetime.now()
    se.eventid = event
    try:
        conf = ScoringEngine.utils.getServiceConfig(session, service, server.team)
        servers = conf['servers']
        ser = random.choice(servers)
        dnsentry = ser['dns']
        ip = ser['ip']
        sp = subprocess.Popen(["nslookup",dnsentry,server.getIP()],stdout=subprocess.PIPE)
        lines = sp.stdout
        sp.wait()
        l = lines.readLines()

        for line in l[2:]:
            if line.contains(ip):
                se.up = True
                return

        print "bad"
    except Exception as e:
        se.info = e.message
        se.up = False
        pass
    session.add(se)
    session.commit()
    session.close()