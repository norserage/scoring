import ScoringEngine.db.tables as tables
from ScoringEngine.db import Session
import ScoringEngine.utils as utils
import json
from datetime import datetime
import paramiko

def test(server, service, event):
    #raise NotImplementedError();
    session=Session()
    se = tables.ScoreEvent()
    se.serviceid = service.id;
    se.teamserverid = server.id;
    se.scoretime = datetime.now()
    se.eventid = event
    ssh = paramiko.SSHClient()
    try:
        
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server.getIP(), username="chip",password="aaaa")

        se.up = True
    except Exception as e:
        se.info = e.message
        se.up = False
    finally:
        ssh.close()
    session.add(se)
    session.commit()
    session.close()
