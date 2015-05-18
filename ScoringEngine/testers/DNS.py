import ScoringEngine.db.tables as tables
from ScoringEngine.db import Session
import json
import ScoringEngine.utils
import subprocess
import random
from datetime import datetime

def test(server, service):
    session = Session()
    se = tables.ScoreEvent()
    se.serviceid = service.id;
    se.teamserverid = server.id;
    se.scoretime = datetime.now()
    try:
        confpair = session.query(tables.ServiceArg).filter(tables.and_(tables.ServiceArg.serviceid==service.id,tables.ServiceArg.key==server.team.id+'conf'))
        conf = json.loads(confpair.value)
        servers = conf['servers']
        ser = random.choice(servers)
        #ser = servers[random.randint(0,servers.length)]
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
