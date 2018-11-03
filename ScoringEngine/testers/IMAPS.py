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
import imaplib
import ScoringEngine.core.db.tables as tables
from ScoringEngine.core.db import Session
from ScoringEngine.core import logger
import ScoringEngine.utils as utils
import ScoringEngine.engine.options
from datetime import datetime

def test(server, service, event):
    session=Session()
    se = tables.ScoreEvent()
    se.serviceid = service.id;
    se.teamserverid = server.id;
    se.scoretime = datetime.now()
    se.eventid = event
    try:
        imap = imaplib.IMAP4_SSL(server.getIP())
        conf = utils.getServiceConfig(session, service, server)
        if 'passdb' not in conf:
            logger.warning("Service %i is not configured" % service.id)
            session.close()
            return
        user = utils.getRandomUser(session, conf['passdb'])
        r = imap.login(user['email'], user['pass'])
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
        'passdb': ScoringEngine.engine.options.PasswordDB()
        }