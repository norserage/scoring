import ScoringEngine.db.tables as tables
from ScoringEngine.db import Session
import ScoringEngine.utils as utils
import json
from datetime import datetime
import socket

def test(server, service, event):
    #raise NotImplementedError();
    session=Session()
    se = tables.ScoreEvent()
    se.serviceid = service.id;
    se.teamserverid = server.id;
    se.scoretime = datetime.now()
    se.eventid = event
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((server.getIP(), service.port))
        se.up = True
        se.info = s.recv(1024)
    except Exception as e:
        se.info = e.message
        se.up = False
    finally:
        s.close()
    session.add(se)
    session.commit()
    session.close()
