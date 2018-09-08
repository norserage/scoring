
from datetime import datetime
from flask import render_template, session
from ScoringEngine.web import app
from ScoringEngine.core.db import Session
from ScoringEngine.core.db import tables


@app.route('/inject/admin')
def inject_events():
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