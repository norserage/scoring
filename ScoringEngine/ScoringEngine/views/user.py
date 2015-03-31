from datetime import datetime
from flask import render_template, request, session, redirect
from ScoringEngine import app
from ScoringEngine.db import session
import ScoringEngine.db.tables as tables
import ScoringEngine.utils
import Crypto

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        users = session.query(tables.TeamUser).filter(tables.TeamUser.username.like(request.form['username']))
        p = Crypto.Hash.MD5.new(request.form['password'])
        for user in users:
            if user.password == p:
                #TODO create user session
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

@app.route('/user/<name>')
def viewuser(name):
    """Renders the home page."""
    return render_template(
        'user/view.html',
        title='Home Page',
        year=datetime.now().year,
    )

