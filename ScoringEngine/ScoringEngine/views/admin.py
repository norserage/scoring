from datetime import datetime
from flask import render_template, request, session, redirect
from ScoringEngine import app
from ScoringEngine.db import session as dbsession
import ScoringEngine.db.tables as tables
import ScoringEngine.utils

@app.route('/admin')
def admin():
    """Renders the home page."""
    return render_template(
        'admin/index.html',
        title='Home Page',
        year=datetime.now().year,
        enginestatus=ScoringEngine.engine.running,
        user=session['user'],
        login='user' in session,
    )

@app.route('/admin/team')
def team():
    teams = dbsession.query(tables.Team).all()
    """Renders the home page."""
    return render_template(
        'admin/team/list.html',
        title='Home Page',
        year=datetime.now().year,
        enginestatus=ScoringEngine.engine.running,
        user=session['user'],
        login='user' in session,
        teams=teams
    )

@app.route('/admin/team/add',methods=['GET','POST'])
def addteam():
    """Renders the home page."""
    return render_template(
        'admin/team/add.html',
        title='Home Page',
        year=datetime.now().year,
        enginestatus=ScoringEngine.engine.running,
        user=session['user'],
        login='user' in session,
    )

@app.route('/admin/team/<team>')
def teamid(team):
    """Renders the home page."""
    return render_template(
        'admin/team/view.html',
        title='Home Page',
        year=datetime.now().year,
        enginestatus=ScoringEngine.engine.running,
        user=session['user'],
        login='user' in session,
    )

@app.route('/admin/scoring/<flag>')
def adminscoringswitch(flag):
    if flag == "true":
        ScoringEngine.engine.running = True
        ScoringEngine.engine.start()
        return ""
    else:
        ScoringEngine.engine.running = False
        return ""

