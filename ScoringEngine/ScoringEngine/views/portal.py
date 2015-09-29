from datetime import datetime
from flask import render_template, request, session, redirect
from ScoringEngine.web import app
from ScoringEngine.db import Session
import ScoringEngine.db.tables as tables
import ScoringEngine.utils

@app.route('/portal')
def portal():
    dbsession = Session()
    data=[]
    stmt = tables.exists().where(tables.Server.id==tables.TeamServer.serverid)
    servers = dbsession.query(tables.Server).filter(tables.and_(stmt,tables.Server.enabled == True))
    if session['user']['group'] > 1:
        teams = dbsession.query(tables.Team).filter(tables.Team.enabled == True)
    else:
        teams = dbsession.query(tables.Team).filter(tables.and_(tables.Team.enabled == True,tables.Team.id == session["user"]["team"])).order_by(tables.Team.name)
    for team in teams:
        row = []
        row.append(team.name)
        for server in servers:
            teamservers = dbsession.query(tables.TeamServer).filter(tables.and_(tables.TeamServer.serverid == server.id,tables.TeamServer.teamid == team.id))
            for service in server.services:
                if service.enabled:
                    if teamservers.count() > 0:
                        teamserver = teamservers[0]
                        score = dbsession.query(tables.ScoreEvent).filter(tables.and_(tables.ScoreEvent.serviceid == service.id, tables.ScoreEvent.teamserverid == teamserver.id)).order_by(tables.ScoreEvent.scoretime.desc()).limit(1)
                        if score.count() > 0:
                            s = score[0]
                            if s.up:
                                row.append("up")
                            else:
                                row.append("down")
                        else:
                            row.append("")
                    else:
                        row.append(None)
        data.append(row)

    return render_template(
        'portal/index.html',
        title='Portal',
        year=datetime.now().year,
        user=session['user'],
        login='user' in session,
        data=data,
        servers=servers
    )

