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
        r = utils.Ping(server.getIP(), 5)
        if r:
            se.up = True
            se.info = json.dumps({'trip': r})
        else:
            se.up = False
    except Exception as e:
        se.info = e.message
        se.up = False
    session.add(se)
    session.commit()
    session.close()

def options():
    return {
        
        }
