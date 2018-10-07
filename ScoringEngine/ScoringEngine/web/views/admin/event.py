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

        sd = dbsession.query(tables.Team.name, tables.func.sum(tables.expression.case(value=tables.ScoreEvent.up, whens={True: 1, False: 0})), tables.func.count(tables.ScoreEvent.id)).select_from(tables.ScoreEvent).filter(tables.ScoreEvent.eventid == event.id).join(tables.TeamServer).join(tables.Team).group_by(tables.Team.name).order_by(tables.Team.name)

        #scoredata = dbsession.execute(tables.text("select t.name, sum(case when se.up = true then 1 else 0 end), count(se.id), round((sum(case when se.up = true then 1.0 else 0.0 end)/count(se.id)) * 100.0, 2) from scoreevents se inner join teamservers ts on ts.id = se.teamserverid inner join teams t on ts.teamid = t.id where se.eventid = " + str(event.id) + " group by t.name order by t.name"))

        return render_template(
            'admin/event/view.html',
            title=event.name,
            year=datetime.now().year,
            event=event,
            scoredata=sd
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
    event = dbsession.query(tables.Event).filter(tables.Event.id == event).first()
    if event:
        if request.method == "POST":
            event.name = request.form['name']
            dbsession.commit()
            return redirect(url_for('events'))
        return render_template(
            "admin/event/edit.html",
            title="Edit Event " + str(event.id),
            event=event
        )
    else:
        from ScoringEngine.web.views.errors import page_not_found
        return page_not_found(None)


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
                    e.end = datetime.utcnow()
        event.current = True
        event.start = datetime.utcnow()
        dbsession.commit()
        return redirect(url_for("events"))
    else:
        from ScoringEngine.web.views.errors import page_not_found
        return page_not_found(None)

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
        event.end = datetime.utcnow()
        dbsession.commit()
        return redirect(url_for("events"))
    else:
        from ScoringEngine.web.views.errors import page_not_found
        return page_not_found(None)