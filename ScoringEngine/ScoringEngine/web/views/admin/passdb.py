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
import Crypto.Hash.MD5
import csv

from ScoringEngine.web.flask_utils import db_user, require_group
from flask_login import current_user, login_required


@app.route('/admin/passdb')
@login_required
@require_group(4)
@db_user
def passdbs():
    dbsession = getSession()
    passdblist = dbsession.query(tables.PasswordDatabase).order_by(tables.PasswordDatabase.name)

    return render_template(
        'admin/passdb/list.html',
        title='Password Databases',
        year=datetime.now().year,
        passdblist=passdblist
    )

@app.route('/admin/passdb/add',methods=['GET','POST'])
@login_required
@require_group(4)
@db_user
def addpassdb():
    dbsession = getSession()
    if request.method == 'POST':
        db = tables.PasswordDatabase()
        db.name = request.form["name"]
        db.domain = request.form["domain"]

        dbsession.add(db)
        dbsession.commit()
        return redirect(url_for('passdbs'))
    else:
        teams = dbsession.query(tables.Team).all()
        return render_template(
            'admin/passdb/add.html',
            title='Add Password Database',
            year=datetime.now().year,
        )

@app.route('/admin/passdb/<passdb>')
@login_required
@require_group(4)
@db_user
def passdb(passdb):
    dbsession = getSession()
    passdbs = dbsession.query(tables.PasswordDatabase).filter(tables.PasswordDatabase.name.ilike(passdb))
    if passdbs.count() > 0:
        passdb = passdbs[0]
        return render_template(
            'admin/passdb/view.html',
            title=passdb.name,
            year=datetime.now().year,
            passdb=passdb,
        )
    else:
        return render_template(
            'admin/404.html',
            title='404 User Not Found',
            year=datetime.now().year,
            message="We could not find the user that you were looking for."
        )

@app.route('/admin/passdb/<passdb>/edit',methods=['GET','POST'])
@login_required
@require_group(4)
@db_user
def editpassdb(passdb):
    dbsession = getSession()
    users = dbsession.query(tables.User).filter(tables.User.name.ilike(passdb))
    if users.count() > 0:
        dbuser = users[0]
        if request.method == 'POST':
            dbuser.name = request.form["name"]
            dbuser.username = request.form["username"]
            dbuser.team = request.form["team"]
            dbuser.group = request.form["group"]
            if str(request.form["password"]).strip() != "":
                m = Crypto.Hash.MD5.new()
                m.update(request.form["password"])
                dbuser.password = m.hexdigest()
            #team.save()
            dbsession.commit()
            return redirect(url_for('adminuser',user=dbuser.name))
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
        return render_template(
            'admin/404.html',
            title='404 User Not Found',
            year=datetime.now().year,
            message="We could not find the user that you were looking for."
        )

@app.route('/admin/passdb/<passdb>/import',methods=['GET','POST'])
@login_required
@require_group(4)
@db_user
def importpassdb(passdb):
    dbsession = getSession()
    db = dbsession.query(tables.PasswordDatabase).filter(tables.PasswordDatabase.name.ilike(passdb)).first()
    if request.method == 'POST':
        file = request.files['file']
        if file:
            datafile = csv.reader(file)
            for line in datafile:
                entry = tables.PasswordDatabaseEntry()
                entry.user, entry.password, entry.email = line[0], line[1], line[2]
                entry.passdbid = db.id
                dbsession.add(entry)
        dbsession.commit()
        return redirect(url_for('passdb',passdb=passdb))
    else:
        teams = dbsession.query(tables.Team).all()
        return render_template(
            'admin/passdb/import.html',
            title='Import Password Database',
            year=datetime.now().year,
        )