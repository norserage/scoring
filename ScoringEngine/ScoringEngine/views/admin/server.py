from datetime import datetime
from flask import render_template, request, session, redirect, url_for, escape
from ScoringEngine.web import app
from ScoringEngine.db import Session
import ScoringEngine.db.tables as tables
import ScoringEngine.utils
import ScoringEngine.engine
from pprint import pprint as pp


@app.route('/admin/server')
def servers():
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
        servers = dbsession.query(tables.Server).all()
        """Renders the home page."""
        return render_template(
            'admin/server/list.html',
            title='Servers',
            year=datetime.now().year,
            enginestatus=ScoringEngine.engine.running,
            user=session['user'],
            login='user' in session,
            servers=servers
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

@app.route('/admin/server/add',methods=['GET','POST'])
def addserver():
    if 'user' in session and session['user']['group'] == 5:
        if request.method == 'POST':
            dbsession = Session()
            s = tables.Server()
            s.name = request.form['name']
            if request.form['ip3'].strip() == "":
                s.ip_3 = None
            else:
                s.ip_3 = request.form['ip3']
            s.ip_4 = request.form['ip4']
            s.enabled = 'enabled' in request.form
            dbsession.add(s)
            dbsession.commit()
            return redirect(url_for('servers'))
        else:
            return render_template(
                'admin/server/add.html',
                title='Add Server',
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

@app.route('/admin/server/<server>')
def server(server):
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
        servers = dbsession.query(tables.Server).filter(tables.Server.id == server)
        if servers.count() > 0:
            server = servers[0]
            return render_template(
                'admin/server/view.html',
                title=server.name,
                year=datetime.now().year,
                user=session['user'],
                login='user' in session,
                server=server,
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

@app.route('/admin/server/<server>/edit',methods=['GET','POST'])
def editserver(server):
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

@app.route('/admin/server/<server>/addservice',methods=['GET','POST'])
def serveraddservice(server):
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
        servers = dbsession.query(tables.Server).filter(tables.Server.id == server)
        if servers.count() > 0:
            server = servers[0]
            if request.method == 'POST':
                s = tables.Service()
                s.serverid = server.id
                s.name = request.form['name']
                s.typeid = request.form['type']
                s.port = request.form['port']
                s.enabled = 'enabled' in request.form
                dbsession.add(s)
                dbsession.commit()
                return redirect(url_for('server',server=server.id))
            else:
                types = dbsession.query(tables.ServiceType).order_by(tables.ServiceType.name.asc()).all()
                return render_template(
                    'admin/server/addservice.html',
                    title='Add Server',
                    year=datetime.now().year,
                    user=session['user'],
                    login='user' in session,
                    types=types,
                    server=server
                )
        else:
            return render_template(
                'admin/404.html',
                title='404 Server Not Found',
                year=datetime.now().year,
                user=session['user'],
                login='user' in session,
                message="We could not find the server that you were looking for."
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