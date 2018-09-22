﻿"""
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

from ScoringEngine.web.flask_utils import db_user, require_group
from flask_login import current_user, login_required


@app.route('/admin/event')
@login_required
@require_group(4)
@db_user
def events():
    dbsession = getSession()
    events = dbsession.query(tables.Event).order_by(tables.Event.id).all()
    return render_template(
        'admin/event/list.html',
        title='Events',
        year=datetime.now().year,
        events=events
    )

@app.route('/admin/event/add',methods=['GET','POST'])
@login_required
@require_group(4)
@db_user
def addevent():
    if request.method == 'POST':
        dbsession = getSession()
        e = tables.Event()
        e.name = request.form['name']
        dbsession.add(e)
        dbsession.commit()
        return redirect(url_for('events'))
    else:
        return render_template(
            'admin/event/add.html',
            title='Add Event',
            year=datetime.now().year,
        )


@app.route('/admin/event/<event>')
@login_required
@require_group(4)
@db_user
def event(event):
    dbsession = getSession()
    events = dbsession.query(tables.Event).filter(tables.Event.id == event)

    if events.count() > 0:
        event = events[0]
        scoredata = dbsession.execute(tables.text("select t.name, sum(case when se.up = true then 1 else 0 end), count(se.id), round((sum(case when se.up = true then 1.0 else 0.0 end)/count(se.id)) * 100.0, 2) from scoreevents se inner join teamservers ts on ts.id = se.teamserverid inner join teams t on ts.teamid = t.id where se.eventid = " + str(event.id) + " group by t.name order by t.name"))

        return render_template(
            'admin/event/view.html',
            title=event.name,
            year=datetime.now().year,
            event=event,
            scoredata=scoredata
        )
    else:
        return render_template(
            'admin/404.html',
            title='404 Team Not Found',
            year=datetime.now().year,
            message="We could not find the team that you were looking for."
        )

@app.route('/admin/event/<event>/edit',methods=['GET','POST'])
@login_required
@require_group(4)
@db_user
def editevent(event):
    dbsession = getSession()
    servers = dbsession.query(tables.Server).filter(tables.Server.id == event)
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
            return redirect(url_for('server', server=server.id))
        else:
            return render_template(
                'admin/server/edit.html',
                title='Edit Team',
                year=datetime.now().year,
                server=server
            )
    else:
        return render_template(
            'admin/404.html',
            title='404 Server Not Found',
            year=datetime.now().year,
            message="We could not find the server that you were looking for."
        )


@app.route('/admin/event/<event>/start')
@login_required
@require_group(4)
@db_user
def startevent(event):
    dbsession = getSession()
    events = dbsession.query(tables.Event).filter(tables.Event.id == event)
    if events.count() > 0:
        event = events[0]
        events = dbsession.query(tables.Event).filter(tables.Event.current == True)
        if events.count() > 0:
            for e in events:
                e.current = False
                if e.end == None:
                    e.end = datetime.now()
        event.current = True
        event.start = datetime.now()
        dbsession.commit()
        return redirect(url_for("events"))
    else:
        return render_template(
            'admin/404.html',
            title='404 Server Not Found',
            year=datetime.now().year,
            message="We could not find the server that you were looking for."
        )

@app.route('/admin/event/<event>/stop')
@login_required
@require_group(4)
@db_user
def stopevent(event):
    dbsession = getSession()
    events = dbsession.query(tables.Event).filter(tables.Event.id == event)
    if events.count() > 0:
        event = events[0]
        event.current = False
        event.end = datetime.now()
        dbsession.commit()
        return redirect(url_for("events"))
    else:
        return render_template(
            'admin/404.html',
            title='404 Server Not Found',
            year=datetime.now().year,
            user=session['user'],
            login='user' in session,
            message="We could not find the server that you were looking for."
        )