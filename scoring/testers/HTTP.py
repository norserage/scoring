import mechanize
import tables
import json
import utils

def test(server, service, session):
    try:
        confpair = session.query(tables.ServiceArg).filter(tables.and_(tables.ServiceArg.serviceid==service.id,tables.ServiceArg.key==server.team.id+'conf'))
        conf = json.loads(confpair.value)
        
    except:
        pass
