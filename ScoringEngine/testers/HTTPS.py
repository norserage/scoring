import mechanize
import ScoringEngine.db.tables as tables
from ScoringEngine.db import session
import ScoringEngine.utils as utils
import json
from datetime import datetime

def test(server, service):
    se = tables.ScoreEvent()
    se.serviceid = service.id;
    se.teamserverid = server.id;
    se.scoretime = datetime.now()
    try:
        #confpair = session.query(tables.ServiceArg).filter(tables.and_(tables.ServiceArg.serviceid==service.id,tables.ServiceArg.key==server.team.id+'conf'))
        #conf = json.loads(confpair.value)
        br = mechanize.Browser()
        br.open("https://"+server.getIP())
        se.up = True
        se.info = br.title()
    except Exception as e:
        se.info = e.message
        se.up = False
    session.add(se)
    session.commit()
