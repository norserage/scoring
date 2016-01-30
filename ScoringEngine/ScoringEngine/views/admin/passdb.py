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
from flask import render_template, request, session, redirect, url_for, escape
from ScoringEngine.web import app
from ScoringEngine.db import Session
import ScoringEngine.db.tables as tables
import ScoringEngine.utils
import ScoringEngine.engine
import Crypto.Hash.MD5
from pprint import pprint as pp
import csv


@app.route('/admin/passdb')
def passdbs():
    if 'user' in session and session['user']['group'] >= 4:
        dbsession = Session()
        passdblist = dbsession.query(tables.PasswordDatabase).order_by(tables.PasswordDatabase.name)
        
        return render_template(
            'admin/passdb/list.html',
            title='Home Page',
            year=datetime.now().year,
            enginestatus=ScoringEngine.engine.running,
            user=session['user'],
            login='user' in session,
            passdblist=passdblist
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

@app.route('/admin/passdb/add',methods=['GET','POST'])
def addpassdb():
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
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
                user=session['user'],
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

@app.route('/admin/passdb/<passdb>')
def passdb(passdb):
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
        passdbs = dbsession.query(tables.PasswordDatabase).filter(tables.PasswordDatabase.name.ilike(passdb))
        if passdbs.count() > 0:
            passdb = passdbs[0]
            return render_template(
                'admin/passdb/view.html',
                title=passdb.name,
                year=datetime.now().year,
                user=session['user'],
                login='user' in session,
                passdb=passdb,
            )
        else:
            return render_template(
                'admin/404.html',
                title='404 User Not Found',
                year=datetime.now().year,
                user=session['user'],
                login='user' in session,
                message="We could not find the user that you were looking for."
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

@app.route('/admin/user/<passdb>/edit',methods=['GET','POST'])
def editpassdb(passdb):
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
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
                    user=session['user'],
                    login='user' in session,
                    dbuser=dbuser,
                    teams=teams
                )
        else:
            return render_template(
                'admin/404.html',
                title='404 User Not Found',
                year=datetime.now().year,
                user=session['user'],
                login='user' in session,
                message="We could not find the user that you were looking for."
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

@app.route('/admin/passdb/<passdb>/import',methods=['GET','POST'])
def importpassdb(passdb):
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
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
                user=session['user'],
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