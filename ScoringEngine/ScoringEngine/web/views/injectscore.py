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

from pyclamd import ClamdNetworkSocket, ClamdUnixSocket, ConnectionError, BufferTooLongError
from ScoringEngine.core import config, logger

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

@app.route('/injectscore/<event>/report')
@login_required
@require_group(3)
@db_user
def inject_score_event_report(event):
    session = getSession()
    injects = session.query(tables.AssignedInject).filter(tables.AssignedInject.eventid == event)
    teams = session.query(tables.Team).all()
    def get_max_score_for_team(team, inject):
        score = session.query(tables.TeamInjectSubmission).filter(tables.TeamInjectSubmission.teamid == team, tables.TeamInjectSubmission.assignedinjectid == inject).order_by(tables.TeamInjectSubmission.points.desc()).first()
        if score:
            return score.points
        return 0

    return render_template(
        'injectscore/report.html',
        title="Inject Scoring",
        injects=injects,
        teams=teams,
        datetime=datetime,
        get_max_score_for_team=get_max_score_for_team
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
        if config.get_item("clam/enabled") and 'ignore_virus' not in request.args:
            if config.get_item("clam/stream_limit") < f.size:
                return render_template(
                    "injectscore/virus_error.html",
                )
            try:
                if config.has_item("clam/path"):
                    cd = ClamdUnixSocket(config.get_item("clam/path"))
                elif config.has_item("clam/address"):
                    cd = ClamdNetworkSocket(config.get_item("clam/address").encode('ascii'), config.get_item("clam/port"))
                cd.ping()
                logger.debug(cd.version())
                virus_info = cd.scan_stream(f.data)
                logger.debug(virus_info)
                if virus_info is not None:
                    return render_template(
                        "injectscore/virus.html",
                        virus_info=virus_info,
                        title="Virus Found"
                    )
            except ConnectionError as ce:
                logger.error(ce.message)
                return render_template(
                    "injectscore/virus_error.html",
                )
            except BufferTooLongError as btle:
                logger.error(btle.message)
                return render_template(
                    "injectscore/virus_error.html",
                )
        r = make_response(f.data)
        r.headers['Content-Disposition'] = 'attachment; filename="' + f.filename + '"'
        r.mimetype='application/octet-stream'
        return r
    from ScoringEngine.web.views.errors import page_not_found
    return page_not_found(None)