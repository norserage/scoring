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
import ScoringEngine.utils as utils
import json
import ScoringEngine.options
from datetime import datetime
import paramiko

def test(server, service, event):
    #raise NotImplementedError();
    session=Session()
    se = tables.ScoreEvent()
    se.serviceid = service.id
    se.teamserverid = server.id
    se.scoretime = datetime.now()
    se.eventid = event
    ssh = paramiko.SSHClient()
    try:
        conf = utils.getServiceConfig(session, service, server)
        if not conf.has_key('passdb'):
            print("WARNING: Service %i not configured" % (service.id))
            ssh.close()
            return
        user = utils.getRandomUser(session, conf['passdb'])
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(server.getIP(), username=user['user'], password=user['pass'])
        ssh.exec_command("ping -c 4 8.8.8.8")
        se.up = True
    except Exception as e:
        se.info = e.message
        se.up = False
    finally:
        ssh.close()
    session.add(se)
    session.commit()
    session.close()


def options():
    return {
        'passdb': ScoringEngine.options.PasswordDB()
        }