__author__ = 'thebmw'

from datetime import datetime
from flask import render_template, session, redirect, url_for
from ScoringEngine.web import app
from ScoringEngine.db import tables, Session



@app.route('/inject/db')
def inject_events():
    raise NotImplementedError()
    dbsession = Session()
    events = dbsession.query(tables.Event).filter(tables.Event.end is not None).order_by(tables.Event.name)
    """Renders the about page."""
    return render_template(
        'injectmanager/index.html',
        title='Inject Manager',
        year=datetime.now().year,
        message='Norser@g3 Inject Scoring Engine',
        user=session['user'],
        login='user' in session,
        events=events
    )