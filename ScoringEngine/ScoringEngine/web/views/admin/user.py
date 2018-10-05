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
from flask import render_template, request, redirect, url_for
from ScoringEngine.web import app
from ScoringEngine.core.db import getSession, tables

from ScoringEngine.web.flask_utils import db_user, require_group
from flask_login import login_required


@app.route('/admin/user')
@login_required
@require_group(4)
@db_user
def users():
    dbsession = getSession()
    users = dbsession.query(tables.User).all()
    """Renders the home page."""
    return render_template(
        'admin/user/list.html',
        title='Users List',
        year=datetime.now().year,
        users=users
    )

@app.route('/admin/user/add',methods=['GET','POST'])
@login_required
@require_group(4)
@db_user
def adduser():
    dbsession = getSession()
    if request.method == 'POST':
        u = tables.User.create(request.form['name'], request.form['username'], request.form['password'], request.form['team'], request.form['group'])
        dbsession.add(u)
        dbsession.commit()
        return redirect(url_for('users'))
    else:
        teams = dbsession.query(tables.Team).all()
        return render_template(
            'admin/user/add.html',
            title='Add Team',
            year=datetime.now().year,
            teams=teams,
        )

@app.route('/admin/user/<user>')
@login_required
@require_group(4)
@db_user
def adminuser(user):
    dbsession = getSession()
    users = dbsession.query(tables.User).filter(tables.User.name.ilike(user))
    if users.count() > 0:
        user = users[0]
        return render_template(
            'admin/user/view.html',
            title=user.name,
            year=datetime.now().year,
            dbuser=user,
        )
    else:
        from ScoringEngine.web.views.errors import page_not_found
        return page_not_found(None)

@app.route('/admin/user/<user>/edit',methods=['GET','POST'])
@login_required
@require_group(4)
@db_user
def edituser(user):
    dbsession = getSession()
    users = dbsession.query(tables.User).filter(tables.User.name.ilike(user))
    if users.count() > 0:
        dbuser = users[0]
        if request.method == 'POST':
            dbuser.name = request.form["name"]
            dbuser.username = request.form["username"]
            dbuser.team = request.form["team"]
            dbuser.group = request.form["group"]
            if str(request.form["password"]).strip() != "":
               dbuser.set_password(request.form['password'])
            dbsession.commit()
            return redirect(url_for('adminuser', user=dbuser.name))
        else:
            teams = dbsession.query(tables.Team).all()
            return render_template(
                'admin/user/edit.html',
                title='Edit Team',
                year=datetime.now().year,
                dbuser=dbuser,
                teams=teams
            )
    else:
        from ScoringEngine.web.views.errors import page_not_found
        return page_not_found(None)
