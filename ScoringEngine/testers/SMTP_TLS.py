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
    try:
        smtp = smtplib.SMTP(server.getIP(), service.port)
        smtp.starttls()
        conf = utils.getServiceConfig(session, service, server.team)
        user = utils.getRandomUser(session, conf['passdb'])
        r = smtp.login(user['user'],user['pass'])
        if r[0] == 235:
            to_email = utils.getRandomEmail(session, conf['passdb'])
            smtp.sendmail(user['email'],to_email,"This is the test ")
            se.up = True
        else:
            se.up = False
        #se.info = smtp.ehlo_msg
    except Exception as ep:
        se.info = ep.message
        se.up = False
    session.add(se)
    session.commit()
    session.close()