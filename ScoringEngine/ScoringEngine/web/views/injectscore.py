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
from flask import render_template, make_response, request
from ScoringEngine.web import app
from ScoringEngine.core.db import getSession, tables
from ScoringEngine.core.db import tables

from ScoringEngine.web.flask_utils import db_user, require_group
from flask_login import current_user, login_required

@app.route('/injectscore')
@login_required
@require_group(3)
@db_user
def inject_score():
    session = getSession()
    events = session.query(tables.Event).filter(tables.or_(tables.Event.current == True, tables.Event.start == None))
    return render_template(
        'injectscore/index.html',
        title="Inject Scoring",
        events=events
    )

@app.route('/injectscore/past')
@login_required
@require_group(3)
@db_user
def inject_score_past():
    session = getSession()
    events = session.query(tables.Event).filter(tables.Event.end != None)
    return render_template(
        'injectscore/index.html',
        title="Inject Scoring",
        events=events
    )

@app.route('/injectscore/<event>')
@login_required
@require_group(3)
@db_user
def inject_score_event(event):
    session = getSession()
    injects = session.query(tables.AssignedInject).filter(tables.AssignedInject.eventid == event)
    return render_template(
        'injectscore/event.html',
        title="Inject Scoring",
        injects=injects,
        datetime=datetime
    )

@app.route('/injectscore/<event>/inject/<inject>')
@login_required
@require_group(3)
@db_user
def inject_score_event_inject(event, inject):
    session = getSession()
    inject = session.query(tables.AssignedInject).filter(tables.AssignedInject.id == inject).first()
    if inject:
        return render_template(
            'injectscore/inject.html',
            title="Score " + inject.subject,
            inject=inject
        )
    from ScoringEngine.web.views.errors import page_not_found
    return page_not_found(None)

@app.route('/injectscore/<event>/inject/<inject>/response/<response>', methods=['GET', 'POST'])
@login_required
@require_group(3)
@db_user
def inject_score_event_inject_response(event, inject, response):
    session = getSession()
    inject = session.query(tables.AssignedInject).filter(tables.AssignedInject.id == inject).first()
    if inject:
        resp = session.query(tables.TeamInjectSubmission).filter(tables.TeamInjectSubmission.id == response).first()
        if resp:
            if request.method == 'POST':
                resp.points = request.form['score']
                session.commit()
            return render_template(
                'injectscore/score.html',
                title="Score " + inject.subject,
                inject=inject,
                resp=resp
            )
    from ScoringEngine.web.views.errors import page_not_found
    return page_not_found(None)

@app.route('/file/<id>')
@login_required
@require_group(3)
@db_user
def file_download(id):
    session = getSession()
    f = session.query(tables.TeamInjectSubmissionAttachment).filter(tables.TeamInjectSubmissionAttachment.id == id).first()
    if f:
        r = make_response(f.data)
        r.headers['Content-Disposition'] = 'attachment; filename="' + f.filename + '"'
        r.mimetype='application/octet-stream'
        return r
    from ScoringEngine.web.views.errors import page_not_found
    return page_not_found(None)