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
from flask import render_template, request
from ScoringEngine.web import app
from ScoringEngine.core.db import getSession, tables
from ScoringEngine.core.db import tables

from ScoringEngine.web.flask_utils import db_user, require_group
from flask_login import current_user, login_required

@app.route('/inject/<id>')
@login_required
@require_group(1)
@db_user
def inject(id):
    session = getSession()
    #select * from assignedinjects where when < now()
    inject = session.query(tables.AssignedInject).filter(tables.AssignedInject.id == id).first()
    return render_template(
        'inject/view.html',
        title=inject.subject,
        year=datetime.now().year,
        inject=inject
    )

@app.route('/inject/<id>/respond', methods=['GET', 'POST'])
@login_required
@require_group(1)
@db_user
def inject_respond(id):
    session = getSession()
    inject = session.query(tables.AssignedInject).filter(tables.AssignedInject.id == id).first()
    if inject:
        if request.method == "POST":
            sub = tables.TeamInjectSubmission()
            sub.assignedinjectid = id
            sub.when = datetime.now()
            sub.body = request.form['body']
            sub.points = 0
            sub.teamid = current_user.team
            session.add(sub)
            session.commit()
            if 'file' in request.files and request.files['file'].filename != '':
                fi = request.files['file']
                f = tables.TeamInjectSubmissionAttachment()
                f.teaminjectid = sub.id
                f.filename = fi.filename
                f.data = fi.read()
                f.size = len(f.data)
                if f.size > 25e7:
                    # File is too big
                    pass
                session.add(f)
                session.commit()
        return render_template(
            'inject/respond.html',
            title=inject.subject,
            year=datetime.now().year,
            inject=inject
        )
    from ScoringEngine.web.views.errors import page_not_found
    return page_not_found(None)
