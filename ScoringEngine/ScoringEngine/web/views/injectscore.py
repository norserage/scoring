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
from flask import render_template, make_response, request, redirect, url_for
from ScoringEngine.web import app
from ScoringEngine.core.db import getSession, tables
from ScoringEngine.web.views.errors import page_not_found

from ScoringEngine.web.flask_utils import db_user, require_group
from flask_login import current_user, login_required

from ScoringEngine.web.views.errors import page_not_found

from ScoringEngine.core import config

import pytz

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
    event = session.query(tables.Event).filter(tables.Event.id == event).first()
    if event:
        injects = session.query(tables.AssignedInject).filter(tables.AssignedInject.eventid == event.id)
        return render_template(
            'injectscore/event.html',
            title="Inject Scoring",
            injects=injects,
            datetime=datetime,
            event=event
        )
    return page_not_found(None)


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
    event = session.query(tables.Event).filter(tables.Event.id == event).first()
    if inject:
        return render_template(
            'injectscore/inject.html',
            title="Score " + inject.subject,
            inject=inject,
            event=event
        )
    return page_not_found(None)

@app.route('/injectscore/<event>/inject/<inject>/edit', methods=['GET', 'POST'])
@login_required
@require_group(3)
def inject_score_event_inject_edit(event, inject):
    session = getSession()
    inject = session.query(tables.AssignedInject).filter(tables.AssignedInject.id == inject).first()
    if inject:
        if request.method == "POST":
            inject.subject = request.form['subject']
            inject.duration = request.form['duration']
            tz = pytz.timezone(config.get_item("default_timezone"))
            if "timezone" in current_user.settings:
                tz = pytz.timezone(current_user.settings['timezone'])
            localwhen = tz.localize(datetime.strptime(request.form['when'], '%Y-%m-%d %H:%M'))
            inject.when = localwhen.astimezone(pytz.UTC)
            inject.points = request.form['points']
            inject.body = request.form['body']
            session.commit()
        categories = session.query(tables.InjectCategory).filter(tables.InjectCategory.parentid == None)
        event = session.query(tables.Event).filter(tables.Event.id == event).first()
        return render_template(
            "injectscore/edit_inject.html",
            inject=inject,
            event=event,
            categories=categories
        )
    return page_not_found(None)


@app.route('/injectscore/<event>/inject/<inject>/delete', methods=['GET', 'POST'])
@login_required
@require_group(3)
def inject_score_event_inject_remove(event, inject):
    session = getSession()
    inject = session.query(tables.AssignedInject).filter(tables.AssignedInject.id == inject).first()
    if inject:
        if request.method == "POST":
            session.delete(inject)
            session.commit()
            return redirect(url_for('inject_score_event', event=event))
        return render_template(
            "injectscore/delete_inject.html",
            inject=inject,
            event=event
        )
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
                'injectscore/inject.html',
                title="Score " + inject.subject,
                inject=inject,
                event=event
            )
    return page_not_found(None)


@app.route('/injectscore/<event>/inject/<inject>/response/<response>', methods=['GET', 'POST'])
@login_required
@require_group(3)
@db_user
def inject_score_event_inject_response2(event, inject, response):
    session = getSession()
    event = session.query(tables.Event).filter(tables.Event.id == event).first()
    if event:
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
                    resp=resp,
                    event=event
                )
    return page_not_found(None)
