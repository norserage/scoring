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
        conf = ScoringEngine.utils.getServiceConfig(session, service, server)
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