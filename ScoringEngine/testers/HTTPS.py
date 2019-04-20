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
import requests
import ScoringEngine.core.db.tables as tables
from ScoringEngine.core.db import Session
import ScoringEngine.engine.options
import ScoringEngine.utils
from datetime import datetime

def test(server, service, event):
    session=Session()
    se = tables.ScoreEvent()
    se.serviceid = service.id
    se.teamserverid = server.id
    se.scoretime = datetime.now()
    se.eventid = event
    try:
        url = "https://"+server.getIP()
        conf = ScoringEngine.utils.getServiceConfig(session, service, server)
        if "url" in conf:
            url += conf['url']
        res = requests.get(url, verify=False)
        if "regex" in conf and conf['regex'].strip() != "":
            import re
            if re.search(conf['regex'], res.content) is None:
                se.up = False
            else:
                se.up = True
        else:
            se.up = True
    except Exception as e:
        se.info = e.message
        se.up = False
    session.add(se)
    session.commit()
    session.close()

def options():
    return {
        'url': ScoringEngine.engine.options.String(),
        'regex': ScoringEngine.engine.options.String()
        }