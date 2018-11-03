from datetime import datetime
from flask import render_template, session
from ScoringEngine.web import app
from ScoringEngine.core.db import getSession, tables
from ScoringEngine.web.flask_utils import db_user, require_group
from flask_login import current_user, login_required

@app.route("/report/event_total")
@login_required
@require_group(3)
@db_user
def report_event_total_index():
    events = getSession().query(tables.Event).filter(tables.Event.start != None)
    return render_template(
        "report/event_total/index.html",
        title="Event Total Report",
        events=events
    )

@app.route("/report/event_total/<event>")
@login_required
@require_group(3)
@db_user
def report_event_total_report(event):

    data = []

    total = {}

    score_total = getSession().query(tables.func.sum(tables.AssignedInject.points)).filter(tables.AssignedInject.eventid == event).first()

    total['inject'] = score_total[0] if score_total[0] is not None else 0

    injects = getSession().query(tables.AssignedInject).filter(tables.AssignedInject.eventid == event)
    teams = getSession().query(tables.Team).all()
    for team in teams:
        d = {}
        d['team'] = team.name

        # Get the totals for inject points
        d['inject'] = 0
        for inject in injects:
            score = getSession().query(tables.func.max(tables.TeamInjectSubmission.points)).filter(tables.TeamInjectSubmission.teamid == team.id, tables.TeamInjectSubmission.assignedinjectid == inject.id).first()
            d['inject'] += score[0] if score[0] is not None else 0

        uptime = getSession().query(tables.func.count(tables.ScoreEvent.id), tables.func.sum(tables.expression.case(value=tables.ScoreEvent.up, whens={True: 1, False: 0}))).filter(tables.ScoreEvent.eventid==event).join(tables.TeamServer).filter(tables.TeamServer.teamid==team.id).first()

        d['uptime'] = uptime[1] if uptime[1] is not None else 0
        d['total_uptime'] = uptime[0]

        data.append(d)

    return render_template(
        "report/event_total/report.html",
        title="Event Total Report",
        data=data,
        total=total
    )
