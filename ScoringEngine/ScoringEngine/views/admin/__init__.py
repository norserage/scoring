from datetime import datetime
from flask import render_template, request, session, redirect, url_for, escape
from ScoringEngine import app
from ScoringEngine.db import session as dbsession
import ScoringEngine.db.tables as tables
import ScoringEngine.utils
import ScoringEngine.engine
from pprint import pprint as pp

@app.route('/admin')
def admin():
    if 'user' in session and session['user']['group'] == 5:
        return render_template(
            'admin/index.html',
            title='Home Page',
            year=datetime.now().year,
            enginestatus=ScoringEngine.engine.running,
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

@app.route('/admin/scoring/<flag>')
def adminscoringswitch(flag):
    if 'user' in session and session['user']['group'] == 5:
        if flag == "true":
            ScoringEngine.engine.running = True
            ScoringEngine.engine.start()
            return ""
        else:
            ScoringEngine.engine.running = False
            return ""
    else:
        return render_template(
            'errors/403.html',
            title='403 Access Denied',
            year=datetime.now().year,
            user=session['user'],
            login='user' in session,
            message="You do not have permission to use this resource"
        )

