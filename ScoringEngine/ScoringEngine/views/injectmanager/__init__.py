__author__ = 'thebmw'

from datetime import datetime
from flask import render_template, session, redirect, url_for
from ScoringEngine.web import app

@app.route('/inject/admin')
def jhkhkuy():
    """Renders the about page."""
    return render_template(
        'injectmanager/index.html',
        title='About',
        year=datetime.now().year,
        message='Norser@g3 Inject Scoring Engine',
        user=session['user'],
        login='user' in session,
    )