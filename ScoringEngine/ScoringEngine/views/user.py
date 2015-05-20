from datetime import datetime
from flask import render_template, request, session, redirect, url_for
from ScoringEngine.web import app
from ScoringEngine.db import Session
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
        for user in users:
            if str(user.password).lower() == str(p.hexdigest()).lower():
                #TODO create user session
                session["user"] = {'id':user.id,'name':user.name,'group':user.group,'team':user.team,'username':user.username,'groupname':user.getGroupName()}
                print "password correct"
                return redirect("/portal")
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