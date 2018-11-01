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
import ScoringEngine.core.db.tables as tables
from ScoringEngine.core.db import Session
from datetime import datetime
from smb.SMBConnection import SMBConnection
import ScoringEngine.engine.options
import ScoringEngine.utils
from ScoringEngine.core import logger
import json

def test(server, service, event):
    #raise NotImplementedError();
    session=Session()
    se = tables.ScoreEvent()
    se.serviceid = service.id;
    se.teamserverid = server.id;
    se.scoretime = datetime.now()
    se.eventid = event

    try:
        conf = ScoringEngine.utils.getServiceConfig(session, service, server)
        if 'passdb' not in conf or 'share' not in conf or 'path' not in conf or 'file' not in conf or 'remote_name' not in conf:
            logger.warning("No configuration for service %i", service.id)
            session.close()
            return
        user = ScoringEngine.utils.getRandomUser(session, conf['passdb'])
        conn = SMBConnection(user['user'], user['pass'], 'LepusISE', conf['remote_name'], user['domain'], is_direct_tcp=service.port==445)
        if conn.connect(server.getIP(), service.port):
            files = conn.listPath(conf['share'], conf['path'])
            for file in files:
                if file.filename == conf['file']:
                    se.up = True
                    se.info = json.dumps([file.filename for file in files])
        else:
            se.up = False
        conn.close()
    except Exception as e:
        se.up = False
        se.info = e.message
    session.add(se)
    session.commit()
    session.close()

def options():
    return {
        'passdb': ScoringEngine.engine.options.PasswordDB(),
        'remote_name': ScoringEngine.engine.options.String(),
        'share': ScoringEngine.engine.options.String(),
        'path': ScoringEngine.engine.options.String(),
        'file': ScoringEngine.engine.options.String()
        }