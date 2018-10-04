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
from ScoringEngine.web.flask_utils import db_user, require_group
from flask_login import current_user, login_required


@app.route('/admin/server')
@login_required
@require_group(4)
@db_user
def servers():
        dbsession = getSession()
        servers = dbsession.query(tables.Server).all()
        """Renders the home page."""
        return render_template(
            'admin/server/list.html',
            title='Servers',
            year=datetime.now().year,
            servers=servers
        )

@app.route('/admin/server/add',methods=['GET','POST'])
@login_required
@require_group(4)
@db_user
def addserver():
    if request.method == 'POST':
        dbsession = getSession()
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
        )

@app.route('/admin/server/<server>')
@login_required
@require_group(4)
@db_user
def server(server):
    dbsession = getSession()
    servers = dbsession.query(tables.Server).filter(tables.Server.id == server)
    if servers.count() > 0:
        server = servers[0]
        return render_template(
            'admin/server/view.html',
            title=server.name,
            year=datetime.now().year,
            server=server,
        )
    else:
        from ScoringEngine.web.views.errors import page_not_found
        return page_not_found(None)

@app.route('/admin/server/<server>/edit',methods=['GET','POST'])
@login_required
@require_group(4)
@db_user
def editserver(server):
    dbsession = getSession()
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
            dbsession.commit()
            return redirect(url_for('server',server=server.id))
        else:
            return render_template(
                'admin/server/edit.html',
                title='Edit Team',
                year=datetime.now().year,
                server=server
            )
    else:
        from ScoringEngine.web.views.errors import page_not_found
        return page_not_found(None)

@app.route('/admin/server/<server>/addservice',methods=['GET','POST'])
@login_required
@require_group(4)
@db_user
def serveraddservice(server):
    dbsession = getSession()
    servers = dbsession.query(tables.Server).filter(tables.Server.id == server)
    if servers.count() > 0:
        server = servers[0]
        if request.method == 'POST':
            s = tables.Service()
            s.serverid = server.id
            s.name = request.form['name']
            s.typeid = request.form['type']
            if request.form['port'] != "":
                s.port = request.form['port']
            s.enabled = 'enabled' in request.form
            dbsession.add(s)
            dbsession.commit()
            return redirect(url_for('server',server=server.id))
        else:
            types = dbsession.query(tables.ServiceType).order_by(tables.ServiceType.name.asc()).all()
            return render_template(
                'admin/server/addservice.html',
                title='Add Service',
                year=datetime.now().year,
                types=types,
                server=server
            )
    else:
        from ScoringEngine.web.views.errors import page_not_found
        return page_not_found(None)

@app.route('/admin/server/<server>/editservice/<service>',methods=['GET','POST'])
@login_required
@require_group(4)
@db_user
def servereditservice(server,service):
    dbsession = getSession()
    services = dbsession.query(tables.Service).filter(tables.Service.id == service)
    if services.count() > 0:
        service = services[0]
        if request.method == 'POST':
            service.name = request.form['name']
            service.typeid = request.form['type']
            if request.form['port'] != "":
                service.port = request.form['port']
            service.enabled = 'enabled' in request.form
            dbsession.commit()
            return redirect(url_for('server',server=server))
        else:
            types = dbsession.query(tables.ServiceType).order_by(tables.ServiceType.name.asc()).all()
            return render_template(
                'admin/server/editservice.html',
                title='Edit Server',
                year=datetime.now().year,
                types=types,
                service=service
            )
    else:
        from ScoringEngine.web.views.errors import page_not_found
        return page_not_found(None)