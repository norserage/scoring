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
from flask_login import login_user, logout_user, current_user, login_required
from ScoringEngine.web.flask_utils import db_user, require_group
from ScoringEngine.core import logger, config
import pytz

from ScoringEngine import VERSION


def do_login(user):
    login_user(user)
    if 'tmp_user' in session:
        session.pop('tmp_user')
    next = request.args.get("next")
    # if not is_safe_url(next):
    #     return redirect(url_for('index'))
    return redirect(next or url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
@db_user
def login():
    if request.method == 'POST':
        users = getSession().query(tables.User).filter(tables.User.username == request.form['username'])
        for user in users:
            if user.verify_password(request.form['password']):
                logger.debug("Login for " + user.username)
                return do_login(user)
            else:
                logger.warning("Incorrect password for " + user.username)
        return render_template(
            'user/login.html',
            title='Home Page',
            year=datetime.now().year,
            error="User/Password Incorrect",
        )
    return render_template(
        'user/login.html',
        title='Home Page',
        year=datetime.now().year,
        VERSIONSTR=VERSION,
    )


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route('/user/<user>', methods=['GET', 'POST'])
@login_required
@require_group(1)
@db_user
def user(user):
    user = getSession().query(tables.User).filter(tables.User.username.ilike(user)).first()
    if user:
        if user.id == current_user.id or current_user.group >= 4:
            if request.method == "POST":
                if request.form['password'] != "":
                    user.set_password(request.form['password'])
                user.name = request.form['name']
                user.set_user_setting("timezone", request.form['timezone'])
                getSession().commit()
            return render_template(
                'user/view.html',
                title='Home Page',
                year=datetime.now().year,
                dbuser=user,
                timezones=pytz.common_timezones,
                config=config
            )
        else:
            return render_template(
                'errors/403.html',
                title='403 Access Denied',
                year=datetime.now().year,
                message="You do not have permission to use this resource"
            )
    else:
        from ScoringEngine.web.views.errors import page_not_found
        return page_not_found(None)

