import tables
import json
import utils
import subprocess
import random

def test(server, service, session):
    try:
        confpair = session.query(tables.ServiceArg).filter(tables.and_(tables.ServiceArg.serviceid==service.id,tables.ServiceArg.key==server.team.id+'conf'))
        conf = json.loads(confpair.value)
        servers = conf['servers']
        ser = servers[random.randint(0,servers.length)]
        dnsentry = ser['dns']
        ip = ser['ip']
        sp = subprocess.Popen(["nslookup",dnsentry,server.getIP()],stdout=subprocess.PIPE)
        lines = sp.sdtout
        sp.wait()
        l = lines.readLines()

        for i in range(2,l.length-1):
            line = l[i]
            if (line.contains(ip)):
                print "good"
                return

        print "bad"
    except:
        pass
