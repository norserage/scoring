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
        #confpair = session.query(tables.ServiceArg).filter(tables.and_(tables.ServiceArg.serviceid==service.id,tables.ServiceArg.key==server.team.id+'conf'))
        #conf = json.loads(confpair.value)
        r = utils.Ping(server.getIP(), 5)
        if r:
            se.up = True
            se.info = json.dumps({trip:r})
        else:
            se.up = False
    except Exception as e:
        se.info = e.message
        se.up = False
    session.add(se)
    session.commit()
