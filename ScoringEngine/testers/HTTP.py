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
import mechanize
import ScoringEngine.db.tables as tables
from ScoringEngine.db import Session
import ScoringEngine.utils
import json
import ScoringEngine.options
from datetime import datetime

def test(server, service, event):
    session=Session()
    se = tables.ScoreEvent()
    se.serviceid = service.id
    se.teamserverid = server.id
    se.scoretime = datetime.now()
    se.eventid = event
    br = mechanize.Browser()
    try:
        url = "http://"+server.getIP()
        conf = ScoringEngine.utils.getServiceConfig(session, service, server)
        print(json.dumps(conf))
        if conf.has_key("url"):
            url += conf['url']
        br.set_handle_robots(False)
        res = br.open(url)
        contents = res.read()
        if conf.has_key("regex"):
            import re
            if re.search(conf['regex'], contents) == None:
                se.up = False
            else:
                se.up = True
        else:
            se.up = True
        
    except Exception as e:
        se.info = e.message
        se.up = False
    finally:
        br.close()
    session.add(se)
    session.commit()
    session.close()

def options():
    return {
        'url': ScoringEngine.options.String(),
        'regex': ScoringEngine.options.String()
        }