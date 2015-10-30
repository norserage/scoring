import ftplib
import ScoringEngine.db.tables as tables
from ScoringEngine.db import Session
import ScoringEngine.utils as utils
import json
from datetime import datetime

def test(server, service, event):
    session=Session()
    se = tables.ScoreEvent()
    se.serviceid = service.id;
    se.teamserverid = server.id;
    se.scoretime = datetime.now()
    se.eventid = event
    ftp = ftplib.FTP()
    try:
        #ftp = ftplib.FTP(server.getIP())
        ftp.connect(server.getIP())
        conf = ScoringEngine.utils.getServiceConfig(session, service, server.team)
        user = utils.getRandomUser(session, conf['passdb'])
        ftp.login(user['user'],user['pass'])
        
        if conf.has_key('mode') and conf['mode'] != 'connect':
            path = conf['path']
            if conf['mode'] == 'chkfileexist':
                pass
        else:
            se.up = True
            se.info = ftp.nlst()
    except ftplib.error_perm as ep:
        se.info = ep.message
        se.up = False
    finally:
        ftp.close()
    session.add(se)
    session.commit()
    session.close()