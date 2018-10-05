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

from ScoringEngine.core import config

from ScoringEngine.core.db import getSession, tables
from flask import render_template, session, redirect, url_for, request
from ScoringEngine.web import app

from ScoringEngine.web.flask_utils import db_user, require_group
from flask_login import current_user, login_required

from datetime import datetime
import pytz

@app.route('/injectmanager')
@login_required
@require_group(3)
@db_user
def injectmanager():
    db = getSession()
    categories = db.query(tables.InjectCategory).filter(tables.InjectCategory.parentid == None)
    return render_template(
        'injectmanager/index.html',
        title='Inject Manager',
        categories=categories
    )

@app.route('/injectmanager/addcategory', methods=['GET', 'POST'])
@login_required
@require_group(3)
@db_user
def injectmanager_addcategory():
    db = getSession()
    if request.method == "POST":
        cat = tables.InjectCategory()
        if request.form['category'] != '-1':
            cat.parentid = request.form['category']
        cat.name = request.form['name']
        db.add(cat)
        db.commit()
        return redirect(url_for('injectmanager')+"#"+str(cat.id))
    categories = db.query(tables.InjectCategory).filter(tables.InjectCategory.parentid == None)
    return render_template(
        'injectmanager/addcategory.html',
        title='Add Category',
        categories=categories
    )


@app.route('/injectmanager/addinject', methods=['GET', 'POST'])
@login_required
@require_group(3)
@db_user
def injectmanager_addinject():
    db = getSession()
    if request.method == "POST":
        inject = tables.Inject()
        inject.categoryid = request.form['category']
        inject.subject = request.form['subject']
        inject.duration = request.form['duration']
        inject.points = request.form['points']
        inject.body = request.form['body']
        db.add(inject)
        db.commit()
        return redirect(url_for('injectmanager')+"#"+str(inject.categoryid))
    categories = db.query(tables.InjectCategory).filter(tables.InjectCategory.parentid == None)
    return render_template(
        'injectmanager/addinject.html',
        title='Add Inject',
        categories=categories
    )


@app.route('/ajax/injectmanager_list')
@login_required
@require_group(3)
@db_user
def ajax_injectmanager_list():
    if 'id' in request.args:
        db = getSession()
        injects = db.query(tables.Inject).filter(tables.Inject.categoryid == request.args['id'])
        return render_template(
            'injectmanager/injectlist.html',
            injects=injects
        )
    return ""

@app.route("/injectmanager/inject/<id>")
@login_required
@require_group(3)
@db_user
def injectmanager_inject(id):
    db = getSession()
    inject = db.query(tables.Inject).filter(tables.Inject.id == id).first()
    if inject:
        return render_template(
            'injectmanager/inject.html',
            title="Inject - " + inject.subject,
            inject=inject
        )
    from ScoringEngine.web.views.errors import page_not_found
    return page_not_found(None)

@app.route("/injectmanager/inject/<id>/edit", methods=['GET', 'POST'])
@login_required
@require_group(3)
@db_user
def injectmanager_inject_edit(id):
    db = getSession()
    inject = db.query(tables.Inject).filter(tables.Inject.id == id).first()
    if inject:
        if request.method == "POST":
            inject.categoryid = request.form['category']
            inject.subject = request.form['subject']
            inject.duration = request.form['duration']
            inject.points = request.form['points']
            inject.body = request.form['body']
            db.commit()
            return redirect(url_for('injectmanager_inject', id=inject.id))
        categories = db.query(tables.InjectCategory).filter(tables.InjectCategory.parentid == None)
        return render_template(
            'injectmanager/editinject.html',
            title="Edit Inject - " + inject.subject,
            inject=inject,
            categories=categories
        )
    from ScoringEngine.web.views.errors import page_not_found
    return page_not_found(None)


@app.route("/injectmanager/inject/<id>/assign", methods=['GET', 'POST'])
@login_required
@require_group(3)
@db_user
def injectmanager_inject_assign(id):
    db = getSession()
    if request.method == "POST":
        ai = tables.AssignedInject()
        ai.injectid = id
        tz = pytz.timezone(config.get_item("default_timezone"))
        if "timezone" in current_user.settings:
            tz = pytz.timezone(current_user.settings['timezone'])
        localwhen = tz.localize(datetime.strptime(request.form['when'], '%Y-%m-%d %H:%M'))
        ai.when = localwhen.astimezone(pytz.UTC)
        ai.subject = request.form['subject']
        ai.duration = request.form['duration']
        ai.points = request.form['points']
        ai.body = request.form['body']
        ai.eventid = request.form['event']
        ai.allowlate = 'late' in request.form
        db.add(ai)
        db.commit()
        return redirect(url_for('injectmanager_inject', id=id))
    inject = db.query(tables.Inject).filter(tables.Inject.id == id).first()
    if inject:
        categories = db.query(tables.InjectCategory).filter(tables.InjectCategory.parentid == None)
        events = db.query(tables.Event).filter(tables.Event.end == None)
        return render_template(
            'injectmanager/assigninject.html',
            title="Assign Inject - " + inject.subject,
            inject=inject,
            categories=categories,
            events=events
        )
    from ScoringEngine.web.views.errors import page_not_found
    return page_not_found(None)