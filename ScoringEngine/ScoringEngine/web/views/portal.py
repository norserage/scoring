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
from flask import render_template, session, jsonify
from ScoringEngine.web import app
from ScoringEngine.core.db import session, tables
from ScoringEngine.web.flask_utils import db_user, require_group
from flask_login import current_user, login_required


@app.route('/portal')
@login_required
@require_group(1)
def portal():
    return render_template(
        'portal/index.html',
        title='Portal',
        year=datetime.now().year
    )

@app.route('/score')
@login_required
@require_group(1)
def score_portal():
    return render_template(
        'portal/score.html',
        title='Score Portal',
        year=datetime.now().year
    )

@app.route('/injects')
@login_required
@require_group(1)
def inject_portal():
    return render_template(
        'portal/injects.html',
        title='Inject Portal',
        year=datetime.now().year
    )

@app.route('/portal/score')
@login_required
@require_group(1)
def portal_score():
    data=[]
    stmt = tables.exists().where(tables.Server.id == tables.TeamServer.serverid)
    servers = session.query(tables.Server).filter(tables.and_(stmt, tables.Server.enabled == True)).order_by(
        tables.Server.name)
    if current_user.group > 1:
        teams = session.query(tables.Team).filter(tables.Team.enabled == True).order_by(tables.Team.name)
    else:
        teams = session.query(tables.Team).filter(
            tables.and_(tables.Team.enabled == True, tables.Team.id == current_user.team)).order_by(
            tables.Team.name)
    for team in teams:
        row = []
        row.append(team.name)
        for server in servers:
            teamservers = session.query(tables.TeamServer).filter(
                tables.and_(tables.TeamServer.serverid == server.id, tables.TeamServer.teamid == team.id))
            for service in server.services:
                if service.enabled:
                    if teamservers.count() > 0:
                        teamserver = teamservers[0]
                        score = session.query(tables.ScoreEvent).filter(
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
        'portal/score_table.html',
        title='Portal',
        year=datetime.now().year,
        data=data,
        servers=servers
    )

@app.route('/portal/injects')
@login_required
@require_group(1)
def portal_injects():
    event = tables.Event.current_event()
    if event:
        injects = dbsession.query(tables.AssignedInject).filter(tables.AssignedInject.eventid == event.id).order_by(tables.AssignedInject.when.asc())
    else:
        injects = []

    return render_template(
        'portal/inject_list.html',
        title='Portal',
        year=datetime.now().year,
        injects=injects
    )


@app.route('/portal/injects/json')
@login_required
@require_group(1)
def portal_injects_json():
    event = tables.Event.current_event()
    if event:
        injects = session.query(tables.AssignedInject).filter(tables.AssignedInject.eventid == event.id).order_by(tables.AssignedInject.when.asc())
    else:
        injects = []

    return jsonify([n.json() for n in injects if n.should_show])