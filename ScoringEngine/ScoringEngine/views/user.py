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
from ScoringEngine.db import Session
from ScoringEngine.logger import logger
import ScoringEngine.db.tables as tables
import ScoringEngine.utils
import Crypto.Hash.MD5

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        dbsession = Session()
        users = dbsession.query(tables.User).filter(tables.User.username.like(request.form['username']))
        p = Crypto.Hash.MD5.new()
        p.update(request.form['password'])
        if users.count() == 0:
            logger.logDebug("User", request.form['username'] + " is not a valid user.")
        for user in users:
            if str(user.password).lower() == str(p.hexdigest()).lower():
                #TODO create user session
                session["user"] = {'id':user.id,'name':user.name,'group':user.group,'team':user.team,'username':user.username,'groupname':user.getGroupName()}
                logger.logDebug("User", "Login for " + user.username)
                return redirect("/portal")
            else:
                logger.logDebug("User", "Incorrect Password for " + user.username)
        return render_template(
            'user/login.html',
            title='Home Page',
            year=datetime.now().year,
            error="User/Password Incorrect"
        )
    else:
        return render_template(
            'user/login.html',
            title='Home Page',
            year=datetime.now().year,
        )

@app.route("/logout")
@app.route('/user/logout')
def logout():
    session.pop("user",None)
    return redirect("/")

@app.route('/user/<user>')
def user(user):
    dbsession = Session()
    users = dbsession.query(tables.User).filter(tables.User.username.ilike(user))
    if users.count() > 0:
        user = users[0]
        if user.id == session['user']['id'] or session['user']['group'] >= 4:
            return render_template(
                'user/view.html',
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

@app.route('/user/<user>/changepass',methods=['GET','POST'])
def changeuserpassword(user):
    dbsession = Session()
    users = dbsession.query(tables.User).filter(tables.User.username.ilike(user))
    if users.count() > 0:
        user = users[0]
        if user.id == session['user']['id'] or session['user']['group'] >= 4:
            if request.method == "POST":
                if request.form['password'] == request.form['password2']:
                    m = Crypto.Hash.MD5.new()
                    m.update(request.form["password"])
                    user.password = m.hexdigest()
                    return redirect(url_for("user",user=user.username))
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