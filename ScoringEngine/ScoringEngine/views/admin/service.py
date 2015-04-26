from datetime import datetime
from flask import render_template, request, session, redirect, url_for, escape
from ScoringEngine.web import app
from ScoringEngine.db import Session
import ScoringEngine.db.tables as tables
import ScoringEngine.utils
import ScoringEngine.engine
from pprint import pprint as pp


@app.route('/admin/service')
def services():
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
        services = dbsession.query(tables.ServiceType).all()
        """Renders the home page."""
        return render_template(
            'admin/service/list.html',
            title='Service Types',
            year=datetime.now().year,
            enginestatus=ScoringEngine.engine.running,
            user=session['user'],
            login='user' in session,
            services=services
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

@app.route('/admin/service/add',methods=['GET','POST'])
def addservice():
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


@app.route('/admin/service/<service>/edit',methods=['GET','POST'])
def editservice(service):
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
        servers = dbsession.query(tables.Server).filter(tables.Server.id == server)
        if servers.count() > 0:
            server = servers[0]
            if request.method == 'POST':
                server.name = request.form['name']
                if request.form['ip3'].strip() == "":
                    server.ip_3 = None
                else:
                    server.ip_3 = request.form['ip3']
                server.ip_4 = request.form['ip4']
                server.enabled = 'enabled' in request.form
                #team.save()
                dbsession.commit()
                return redirect(url_for('server',server=server.id))
            else:
                return render_template(
                    'admin/server/edit.html',
                    title='Edit Team',
                    year=datetime.now().year,
                    user=session['user'],
                    login='user' in session,
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
