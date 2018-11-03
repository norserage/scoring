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
from flask import render_template, request, session, redirect, url_for
from ScoringEngine.web import app
from ScoringEngine.core.db import getSession, tables
import ScoringEngine.utils
import ScoringEngine.engine
import json

from ScoringEngine.web.flask_utils import db_user, require_group
from flask_login import login_required

from ScoringEngine.web.views.errors import page_not_found

from ScoringEngine.core import logger


@app.route('/admin/team')
@login_required
@require_group(4)
@db_user
def teams():
    dbsession = getSession()
    teams = dbsession.query(tables.Team).all()
    return render_template(
        'admin/team/list.html',
        title='Team List',
        year=datetime.now().year,
        teams=teams
    )

@app.route('/admin/team/add',methods=['GET','POST'])
@login_required
@require_group(4)
@db_user
def addteam():
    if request.method == 'POST':
        dbsession = getSession()
        t = tables.Team()
        t.name = request.form['name']
        t.network = request.form['network']
        t.enabled = 'enabled' in request.form
        dbsession.add(t)
        dbsession.commit()
        return redirect(url_for('teams'))
    else:
        return render_template(
            'admin/team/add.html',
            title='Add Team',
            year=datetime.now().year,
        )

@app.route('/admin/team/<team>')
@login_required
@require_group(4)
@db_user
def team(team):
    dbsession = getSession()
    teams = dbsession.query(tables.Team).filter(tables.Team.name.ilike(team))
    if teams.count() > 0:
        team = teams[0]
        return render_template(
            'admin/team/view.html',
            title=team.name,
            year=datetime.now().year,
            team=team,
        )
    else:
        from ScoringEngine.web.views.errors import page_not_found
        return page_not_found(None)


@app.route('/admin/team/<team>/edit',methods=['GET','POST'])
@login_required
@require_group(4)
@db_user
def editteam(team):
    dbsession = getSession()
    teams = dbsession.query(tables.Team).filter(tables.Team.name.ilike(team))
    if teams.count() > 0:
        team = teams[0]
        if request.method == 'POST':
            team.name = request.form['name']
            team.network = request.form['network']
            team.enabled = 'enabled' in request.form
            dbsession.commit()
            return redirect(url_for('team', team=team.name))
        else:
            return render_template(
                'admin/team/edit.html',
                title='Edit Team',
                year=datetime.now().year,
                team=team
            )
    else:
        from ScoringEngine.web.views.errors import page_not_found
        return page_not_found(None)


@app.route('/admin/team/<team>/server/add',methods=['GET','POST'])
@login_required
@require_group(4)
@db_user
def teamaddserver(team):
    dbsession = getSession()
    teams = dbsession.query(tables.Team).filter(tables.Team.name.ilike(team))
    if teams.count() > 0:
        team = teams[0]
        if request.method == 'POST':
            s = tables.TeamServer()
            s.serverid = request.form['server']
            s.teamid = team.id
            dbsession.add(s)
            dbsession.commit()
            return redirect(url_for('team', team=team.name))
        else:
            servers = dbsession.query(tables.Server).filter(~tables.Server.teams.any(
                tables.TeamServer.teamid == team.id))
            return render_template(
                'admin/team/addserver.html',
                title='Add Server',
                year=datetime.now().year,
                team=team,
                servers=servers
            )
    else:
        from ScoringEngine.web.views.errors import page_not_found
        return page_not_found(None)


@app.route('/admin/team/<teamid>/server/<serverid>')
@login_required
@require_group(4)
@db_user
def teamserver(teamid, serverid):
    dbsession = getSession()
    logger.debug("teamid: %s" % teamid)
    team = dbsession.query(tables.Team).filter(tables.Team.name == teamid).first()
    if team:
        server = dbsession.query(tables.TeamServer).filter(
            tables.and_(tables.TeamServer.teamid == team.id, tables.TeamServer.serverid == serverid)).first()
        if server:
            return render_template(
                'admin/team/server.html',
                    title='Server',
                    year=datetime.now().year,
                    team=team,
                    server=server
                )
    return page_not_found(None)

@app.route('/admin/team/<teamid>/server/<serverid>/service/<serviceid>',methods=['GET','POST'])
@login_required
@require_group(4)
@db_user
def teamserverservice(teamid, serverid, serviceid):
    dbsession = getSession()
    team = dbsession.query(tables.Team).filter(tables.Team.name.ilike(teamid)).first()
    server = dbsession.query(tables.TeamServer).filter(
        tables.and_(tables.TeamServer.teamid == team.id, tables.TeamServer.serverid == serverid)).first()
    service = dbsession.query(tables.Service).filter(tables.Service.id == serviceid).first()
    m=__import__(service.type.tester)
    func = getattr(m, "options")
    print(service.id)
    print(server.id)
    conf = ScoringEngine.utils.getServiceConfig(dbsession, service, server)
    if request.method == 'POST':
        t = len(conf) == 0
        options=func()
        for key,value in options.iteritems():
            if request.form[key].strip() != "":
                conf[key] = value.parse(request.form[key])
            else:
                if conf.has_key(key):
                    conf[key] = None
        if t:
            confpair = tables.ServiceArg()
            confpair.key = "conf"
            confpair.serverid = server.id
            confpair.serviceid = serviceid
            confpair.value = json.dumps(conf)
            dbsession.add(confpair)
        else: #Conf already exists
            confpair = dbsession.query(tables.ServiceArg).filter(
                tables.and_(tables.ServiceArg.serviceid == service.id, tables.ServiceArg.key == 'conf', tables.ServiceArg.serverid == server.id)).first()
            confpair.value = json.dumps(conf)
        dbsession.commit()
        return redirect(url_for('teamserver', teamid=team.name, serverid=serverid))
    else:
        return render_template(
            'admin/team/service.html',
                title='Server',
                year=datetime.now().year,
                options=func(),
                conf=conf,
                service=service,
                team=team
            )
