from datetime import datetime
from flask import render_template, request, session, redirect, url_for, escape
from ScoringEngine.web import app
from ScoringEngine.db import Session
import ScoringEngine.db.tables as tables
import ScoringEngine.utils
import ScoringEngine.engine
from pprint import pprint as pp
import json


@app.route('/admin/team')
def teams():
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
        teams = dbsession.query(tables.Team).all()
        """Renders the home page."""
        return render_template(
            'admin/team/list.html',
            title='Home Page',
            year=datetime.now().year,
            enginestatus=ScoringEngine.engine.running,
            user=session['user'],
            login='user' in session,
            teams=teams
        )
    else:
        return render_template(
            'errors/403.html',
            title='403 Access Denied',
            year=datetime.now().year,
            user=session['user'],
            login='user' in session,
            message="You do not have permission to use this resource"
        )

@app.route('/admin/team/add',methods=['GET','POST'])
def addteam():
    if 'user' in session and session['user']['group'] == 5:
        if request.method == 'POST':
            dbsession = Session()
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
                user=session['user'],
                login='user' in session,
            )
    else:
        return render_template(
            'errors/403.html',
            title='403 Access Denied',
            year=datetime.now().year,
            user=session['user'],
            login='user' in session,
            message="You do not have permission to use this resource"
        )

@app.route('/admin/team/<team>')
def team(team):
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
        teams = dbsession.query(tables.Team).filter(tables.Team.name.ilike(team))
        if teams.count() > 0:
            team = teams[0]
            return render_template(
                'admin/team/view.html',
                title=team.name,
                year=datetime.now().year,
                user=session['user'],
                login='user' in session,
                team=team,
            )
        else:
            return render_template(
                'admin/404.html',
                title='404 Team Not Found',
                year=datetime.now().year,
                user=session['user'],
                login='user' in session,
                message="We could not find the team that you were looking for."
            )
    else:
        return render_template(
            'errors/403.html',
            title='403 Access Denied',
            year=datetime.now().year,
            user=session['user'],
            login='user' in session,
            message="You do not have permission to use this resource"
        )

@app.route('/admin/team/<team>/edit',methods=['GET','POST'])
def editteam(team):
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
        teams = dbsession.query(tables.Team).filter(tables.Team.name.ilike(team))
        if teams.count() > 0:
            team = teams[0]
            if request.method == 'POST':
                team.name = request.form['name']
                team.network = request.form['network']
                team.enabled = 'enabled' in request.form
                #team.save()
                dbsession.commit()
                return redirect(url_for('team',team=team.name))
            else:
                return render_template(
                    'admin/team/edit.html',
                    title='Edit Team',
                    year=datetime.now().year,
                    user=session['user'],
                    login='user' in session,
                    team=team
                )
        else:
            return render_template(
                'admin/404.html',
                title='404 Team Not Found',
                year=datetime.now().year,
                user=session['user'],
                login='user' in session,
                message="We could not find the team that you were looking for."
            )
    else:
        return render_template(
            'errors/403.html',
            title='403 Access Denied',
            year=datetime.now().year,
            user=session['user'],
            login='user' in session,
            message="You do not have permission to use this resource"
        )

@app.route('/admin/team/<team>/addserver',methods=['GET','POST'])
def teamaddserver(team):
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
        teams = dbsession.query(tables.Team).filter(tables.Team.name.ilike(team))
        if teams.count() > 0:
            team = teams[0]
            if request.method == 'POST':
                s = tables.TeamServer()
                s.serverid = request.form['server']
                s.teamid = team.id
                dbsession.add(s)
                dbsession.commit()
                return redirect(url_for('team',team=team.name))
            else:
                servers = dbsession.query(tables.Server).filter(~tables.Server.teams.any(tables.TeamServer.teamid==team.id))
                return render_template(
                    'admin/team/addserver.html',
                    title='Add Server',
                    year=datetime.now().year,
                    user=session['user'],
                    login='user' in session,
                    team=team,
                    servers=servers
                )
        else:
            return render_template(
                'admin/404.html',
                title='404 Team Not Found',
                year=datetime.now().year,
                user=session['user'],
                login='user' in session,
                message="We could not find the team that you were looking for."
            )
    else:
        return render_template(
            'errors/403.html',
            title='403 Access Denied',
            year=datetime.now().year,
            user=session['user'],
            login='user' in session,
            message="You do not have permission to use this resource"
        )

@app.route('/admin/team/<teamid>/server/<serverid>')
def teamserver(teamid, serverid):
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
        team = dbsession.query(tables.Team).filter(tables.Team.name.ilike(teamid)).first()
        server = dbsession.query(tables.TeamServer).filter(tables.and_(tables.TeamServer.teamid==team.id, tables.TeamServer.serverid==serverid)).first()
        return render_template(
                'admin/team/server.html',
                title='Server',
                year=datetime.now().year,
                user=session['user'],
                login='user' in session,
                team=team,
                server=server
            )
    else:
        return render_template(
            'errors/403.html',
            title='403 Access Denied',
            year=datetime.now().year,
            user=session['user'],
            login='user' in session,
            message="You do not have permission to use this resource"
        )

@app.route('/admin/team/<teamid>/server/<serverid>/service/<serviceid>',methods=['GET','POST'])
def teamserverservice(teamid, serverid, serviceid):
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
        team = dbsession.query(tables.Team).filter(tables.Team.name.ilike(teamid)).first()
        server = dbsession.query(tables.TeamServer).filter(tables.and_(tables.TeamServer.teamid==team.id, tables.TeamServer.serverid==serverid)).first()
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
                                
            if t:
                confpair = tables.ServiceArg()
                confpair.key = "conf"
                confpair.serverid = server.id
                confpair.serviceid = serviceid
                confpair.value = json.dumps(conf)
                dbsession.add(confpair)
            else: #Conf already exists
                confpair = dbsession.query(tables.ServiceArg).filter(tables.and_(tables.ServiceArg.serviceid==service.id,tables.ServiceArg.key=='conf', tables.ServiceArg.serverid==server.id)).first()
                confpair.value = json.dumps(conf)
            dbsession.commit()
        else:
            return render_template(
                    'admin/team/service.html',
                    title='Server',
                    year=datetime.now().year,
                    user=session['user'],
                    login='user' in session,
                    options=func(),
                    conf=conf,
                    service=service
                )
    else:
        return render_template(
            'errors/403.html',
            title='403 Access Denied',
            year=datetime.now().year,
            user=session['user'],
            login='user' in session,
            message="You do not have permission to use this resource"
        )