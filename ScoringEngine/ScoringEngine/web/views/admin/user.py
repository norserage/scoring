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
from ScoringEngine.core.db import Session
import ScoringEngine.core.db.tables as tables
import ScoringEngine.utils
import ScoringEngine.engine
import Crypto.Hash.MD5


@app.route('/admin/user')
def users():
    if 'user' in session and session['user']['group'] >= 4:
        dbsession = Session()
        users = dbsession.query(tables.User).all()
        """Renders the home page."""
        return render_template(
            'admin/user/list.html',
            title='Home Page',
            year=datetime.now().year,
            enginestatus=ScoringEngine.engine.running,
            user=session['user'],
            login='user' in session,
            users=users
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

@app.route('/admin/user/add',methods=['GET','POST'])
def adduser():
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
        if request.method == 'POST':
            p = Crypto.Hash.MD5.new()
            p.update(request.form['password'])
            u = tables.User()
            u.name = request.form['name']
            u.username = request.form['username']
            u.password = p.hexdigest()
            u.team = request.form['team']
            u.group = request.form['group']
            #pp(request.form)
            dbsession.add(u)
            dbsession.commit()
            return redirect(url_for('users'))
        else:
            teams = dbsession.query(tables.Team).all()
            return render_template(
                'admin/user/add.html',
                title='Add Team',
                year=datetime.now().year,
                user=session['user'],
                login='user' in session,
                teams=teams,
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

@app.route('/admin/user/<user>')
def adminuser(user):
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
        users = dbsession.query(tables.User).filter(tables.User.name.ilike(user))
        if users.count() > 0:
            user = users[0]
            return render_template(
                'admin/user/view.html',
                title=user.name,
                year=datetime.now().year,
                user=session['user'],
                login='user' in session,
                dbuser=user,
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

@app.route('/admin/user/<user>/edit',methods=['GET','POST'])
def edituser(user):
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
        users = dbsession.query(tables.User).filter(tables.User.name.ilike(user))
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
