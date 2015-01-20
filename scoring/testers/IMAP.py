import imaplib
import tables
import json
import utils
from datetime import datetime

def test(server, service, session):
    se = tables.ScoreEvent()
    se.serviceid = service.id;
    se.teamserverid = server.id;
    se.scoretime = datetime.now()
    try:
        imap = imaplib.IMAP4(server.getIP())
        confpair = session.query(tables.ServiceArg).filter(tables.and_(tables.ServiceArg.serviceid==service.id,tables.ServiceArg.key==server.team.id+'conf'))
        conf = json.loads(confpair.value)
        user = utils.getRandomUser(session, conf['passdb'])
        imap.login(user['user'],user['pass'])
        se.up = True
    except Exception as ep:
        se.info = ep.message
        se.up = False
    session.add(se)
    