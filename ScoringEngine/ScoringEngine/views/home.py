"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, session, redirect, url_for
from ScoringEngine import app

@app.route('/')
def home():
    if 'user' in session:
        return redirect(url_for("portal"))
    else:
        return redirect(url_for("login"))



@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Norser@g3 Inject Scoring Engine',
        user=session['user'],
        login='user' in session,
    )
