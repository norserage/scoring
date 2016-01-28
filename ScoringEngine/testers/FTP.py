﻿"""
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
import ftplib
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
    ftp = ftplib.FTP()
    try:
        #ftp = ftplib.FTP(server.getIP())
        ftp.connect(server.getIP())
        conf = ScoringEngine.utils.getServiceConfig(session, service, server)
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

def options():
    return {
        'passdb': ScoringEngine.options.PasswordDB()
        }