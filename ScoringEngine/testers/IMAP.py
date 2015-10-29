﻿import imaplib
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
    try:
        imap = imaplib.IMAP4(server.getIP())
        conf = utils.getServiceConfig(session, service, server.team)
        user = utils.getRandomUser(session, conf['passdb'])
        r = imap.login(user['user'],user['pass'])
        if r[0] == 'OK':
            se.up = True
        else:
            se.up = False
    except Exception as ep:
        se.info = ep.message
        se.up = False
    finally:
        imap.close()
    session.add(se)
    session.commit()
    session.close()