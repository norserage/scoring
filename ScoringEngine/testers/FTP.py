import ftplib
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
        ftp = ftplib.FTP(server.getIP())
        confpair = session.query(tables.ServiceArg).filter(tables.and_(tables.ServiceArg.serviceid==service.id,tables.ServiceArg.key==server.team.id+'conf'))
        conf = json.loads(confpair.value)
        user = utils.getRandomUser(session, conf['passdb'])
        ftp.login(user['user'],user['pass'])
        
        if conf.has_key('mode') and conf['mode'] != 'connect':
            path = conf['path']
            if conf['mode'] == 'chkfileexist':
                pass
        else:
            se.up = True
            se.info = ftp.nlst()
    except ftplib.error_perm as ep:
        se.info = ep.message
        se.up = False
    session.add(se)
    