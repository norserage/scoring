"""
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
from datetime import datetime
from flask import render_template, session
from ScoringEngine.web import app
from ScoringEngine.core.db import getSession, tables
from ScoringEngine.web.flask_utils import db_user, require_group
from flask_login import current_user, login_required


@app.route('/portal')
@login_required
@require_group(1)
@db_user
def portal():
    dbsession = getSession()
    data=[]
    stmt = tables.exists().where(tables.Server.id == tables.TeamServer.serverid)
    servers = dbsession.query(tables.Server).filter(tables.and_(stmt, tables.Server.enabled == True)).order_by(
        tables.Server.name)
    if session['user']['group'] > 1:
        teams = dbsession.query(tables.Team).filter(tables.Team.enabled == True).order_by(tables.Team.name)
    else:
        teams = dbsession.query(tables.Team).filter(
            tables.and_(tables.Team.enabled == True, tables.Team.id == session["user"]["team"])).order_by(
            tables.Team.name)
    for team in teams:
        row = []
        row.append(team.name)
        for server in servers:
            teamservers = dbsession.query(tables.TeamServer).filter(
                tables.and_(tables.TeamServer.serverid == server.id, tables.TeamServer.teamid == team.id))
            for service in server.services:
                if service.enabled:
                    if teamservers.count() > 0:
                        teamserver = teamservers[0]
                        score = dbsession.query(tables.ScoreEvent).filter(
                            tables.and_(tables.ScoreEvent.serviceid == service.id, tables.ScoreEvent.teamserverid == teamserver.id)).order_by(
                            tables.ScoreEvent.scoretime.desc()).limit(1)
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
        data=data,
        servers=servers
    )

