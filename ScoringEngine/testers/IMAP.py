import imaplib
import ScoringEngine.db.tables as tables
from ScoringEngine.db import Session
import ScoringEngine.utils as utils
import ScoringEngine.options
import json
from datetime import datetime

def test(server, service, event):
    session=Session()
    se = tables.ScoreEvent()
    se.serviceid = service.id;
    se.teamserverid = server.id;
    se.scoretime = datetime.now()
    se.eventid = event
    
    try:
        imap = imaplib.IMAP4(server.getIP)
        conf = utils.getServiceConfig(session, service, server)
        user = utils.getRandomUser(session, conf['passdb'])
        r = imap.login(user['user'],user['pass'])
        if r[0] == 'OK':
            se.up = True
        else:
            se.up = False
        try:
            imap.close()
        except Exception as ep2:
            pass
    except Exception as ep:
        se.info = ep.message
        se.up = False
    session.add(se)
    session.commit()
    session.close()

def options():
    return {
        'passdb': ScoringEngine.options.PasswordDB()
        }