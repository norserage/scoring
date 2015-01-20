import mechanize
import tables
import json
import utils

def test(server, service, session):
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
        se.info = ep.message
        se.up = False
    session.add(se)
