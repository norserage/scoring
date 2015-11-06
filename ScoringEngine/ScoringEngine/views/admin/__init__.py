from datetime import datetime
from flask import render_template, request, session, redirect, url_for, escape
from ScoringEngine.web import app
from ScoringEngine.conf import conf
from ScoringEngine.db import Session, engine
import ScoringEngine.db.tables as tables
import ScoringEngine.utils
import ScoringEngine.engine
from pprint import pprint as pp

@app.route('/admin')
def admin():
    if 'user' in session and session['user']['group'] >= 4:
        dbsession = Session()
        event = None
        events = dbsession.query(tables.Event).filter(tables.Event.current == True)
        if events.count() > 0:
            event = events[0].id
        return render_template(
            'admin/index.html',
            title='Admin',
            year=datetime.now().year,
            enginestatus=ScoringEngine.engine.running,
            user=session['user'],
            login='user' in session,
            driver=str(engine.driver),
            event=event
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
    if 'user' in session and session['user']['group'] >= 4:
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

