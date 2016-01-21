import ScoringEngine.db.tables as tables
from ScoringEngine.db import Session
import json
import ScoringEngine.utils
import ScoringEngine.options
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
        print json.dumps(ser)
        dnsentry = ser['dns']
        ip = ser['ip']
        sp = subprocess.Popen(["nslookup",dnsentry,server.getIP()],stdout=subprocess.PIPE)
        lines = sp.stdout
        sp.wait()
        l = lines.readlines()

        for line in l[2:]:
            if ip in line:
                print line
                se.up = True
                break
            else:
                se.up = False
        se.info = json.dumps(l)
    except Exception as e:
        se.info = e.message
        se.up = False    
    finally:
        if not se.up:
            se.up = False
    session.add(se)
    session.commit()
    session.close()

def options():
    return {
        'servers': ScoringEngine.options.JSON()
        }