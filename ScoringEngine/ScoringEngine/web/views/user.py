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
from ScoringEngine.logger import logger
from flask_login import login_user, logout_user, current_user, login_required
from ScoringEngine.web.flask_utils import db_user, require_group


def do_login(user):
    tables.UserAuditLogEntry.create(user.id, 'login')
    login_user(user)
    if 'tmp_user' in session:
        session.pop('tmp_user')
    next = request.args.get("next")
    if not is_safe_url(next):
        return redirect(url_for('index'))
    return redirect(next or url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
@db_user
def login():
    if request.method == 'POST':
        db = getSession()
        users = db.query(tables.User).filter(tables.User.username == request.form['username'])
        for user in users:
            if user.verify_password(request.form['password']):
                logger.logDebug("User", "Login for " + user.username)
                return do_login(user)
            else:
                logger.logDebug("User", "Incorrect Password for " + user.username)
        return render_template(
            'user/login.html',
            title='Home Page',
            year=datetime.now().year,
            error="User/Password Incorrect"
        )
    return render_template(
        'user/login.html',
        title='Home Page',
        year=datetime.now().year,
    )


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route('/user/<user>')
@login_required
@require_group(1)
@db_user
def user(user):
    dbsession = getSession()
    user = dbsession.query(tables.User).filter(tables.User.username.ilike(user)).first()
    if user:
        if user.id == current_user.id or current_user.group >= 4:
            return render_template(
                'user/view.html',
                title='Home Page',
                year=datetime.now().year,
                dbuser=user,
            )
        else:
            return render_template(
                'errors/403.html',
                title='403 Access Denied',
                year=datetime.now().year,
                message="You do not have permission to use this resource"
            )
    else:
        return render_template(
            'errors/404.html',
            title='404 Not Found',
            year=datetime.now().year,
            dbuser=user,
            message="We could not find the user you were looking for"
        )


@app.route('/user/<user>/changepass', methods=['GET', 'POST'])
@login_required
@require_group(1)
@db_user
def changeuserpassword(user):
    dbsession = getSession()
    user = dbsession.query(tables.User).filter(tables.User.username.ilike(user)).first()
    if user:
        if user.id == session['user']['id'] or session['user']['group'] >= 4:
            if request.method == "POST":
                if request.form['password'] == request.form['password2']:
                    user.set_password(request.form['password'])
                    return redirect(url_for("user", user=user.username))
                else:
                    return render_template(
                        'user/changepass.html',
                        title='Home Page',
                        year=datetime.now().year,
                        user=session['user'],
                        dbuser=user,
                        login='user' in session,
                        error="Passwords do not match."
                    )
            else:
                return render_template(
                    'user/changepass.html',
                    title='Home Page',
                    year=datetime.now().year,
                    user=session['user'],
                    dbuser=user,
                    login='user' in session,
                )
        else:
            return render_template(
                'errors/403.html',
                title='403 Access Denied',
                year=datetime.now().year,
                user=session['user'],
                login='user' in session,
                message="You do not have permission to use this resource"
            )
    else:
        return render_template(
            'errors/404.html',
            title='404 Not Found',
            year=datetime.now().year,
            user=session['user'],
            dbuser=user,
            login='user' in session,
            message="We could not find the user you were looking for"
        )