from datetime import datetime
from flask import render_template, request, session, redirect
from ScoringEngine import app
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
                session["user"] = {'name':user.name,'group':user.group,'team':user.team,'username':user.username}
                print "password correct"
                return redirect("/portal")
        return render_template(
            'user/login.html',
            title='Home Page',
            year=datetime.now().year,
        )
    else:
        return render_template(
            'user/login.html',
            title='Home Page',
            year=datetime.now().year,
        )

@app.route('/user/<user>')
def user(user):
    """Renders the home page."""
    return render_template(
        'user/view.html',
        title='Home Page',
        year=datetime.now().year,
        user=session['user'],
        login='user' in session,
    )

