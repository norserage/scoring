﻿import smtplib
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
    smtp = smtplib.SMTP_SSL()
    try:
        #smtp = smtplib.SMTP(server.getIP(), service.port)
        smtp.connect(server.getIP(), service.port)
        conf = utils.getServiceConfig(session, service, server.team)
        user = utils.getRandomUser(session, conf['passdb'])
        r = smtp.login(user['email'],user['pass'])
        to_email = utils.getRandomEmail(session, conf['passdb'])
        smtp.sendmail(user['email'],to_email,"This is the test ")
        se.up = True
        
        #se.info = smtp.ehlo_msg
    except Exception as ep:
        se.info = ep.message
        se.up = False
    finally:
        try:
            smtp.close()
        except Exception as ep:
            pass
    session.add(se)
    session.commit()
    session.close()