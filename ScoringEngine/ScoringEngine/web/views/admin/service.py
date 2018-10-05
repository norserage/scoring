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
from pprint import pprint as pp

from ScoringEngine.web.flask_utils import db_user, require_group
from flask_login import current_user, login_required


@app.route('/admin/service')
@login_required
@require_group(4)
@db_user
def services():
    dbsession = getSession()
    services = dbsession.query(tables.ServiceType).all()
    """Renders the home page."""
    return render_template(
        'admin/service/list.html',
        title='Service Types',
        year=datetime.now().year,
        services=services
    )

@app.route('/admin/service/<id>')
@login_required
@require_group(4)
@db_user
def service(id):
    dbsession = getSession()
    service = dbsession.query(tables.ServiceType).filter(tables.ServiceType.id == id).first()
    m=__import__(service.tester)
    func = getattr(m, "options")
    pp(func())
    """Renders the home page."""
    return render_template(
        'admin/service/view.html',
        title='Service Types',
        year=datetime.now().year,
        service=service,
        options=func()
    )

@app.route('/admin/service/add',methods=['GET','POST'])
@login_required
@require_group(4)
@db_user
def addservice():
    if request.method == 'POST':
        dbsession = getSession()
        st = tables.ServiceType()
        st.name = request.form['name']
        st.tester = request.form['tester']
        dbsession.add(st)
        dbsession.commit()
        return redirect(url_for('services'))
    else:
        return render_template(
            'admin/service/add.html',
            title='Add Service Type',
            year=datetime.now().year,
        )


@app.route('/admin/service/<service>/edit',methods=['GET','POST'])
@login_required
@require_group(4)
@db_user
def editservice(service):
    dbsession = getSession()
    services = dbsession.query(tables.ServiceType).filter(tables.ServiceType.id == service)
    if services.count() > 0:
        service = services[0]
        if request.method == 'POST':
            service.name = request.form['name']
            service.tester = request.form['tester']
            dbsession.commit()
            return redirect(url_for('services'))
        else:
            return render_template(
                'admin/service/edit.html',
                title='Edit Team',
                year=datetime.now().year,
                service=service
            )
    else:
        from ScoringEngine.web.views.errors import page_not_found
        return page_not_found(None)
