import mechanize
import ScoringEngine.db.tables as tables
from ScoringEngine.db import Session
import ScoringEngine.utils
import json
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
        conf = ScoringEngine.utils.getServiceConfig(session, service, server.team)
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