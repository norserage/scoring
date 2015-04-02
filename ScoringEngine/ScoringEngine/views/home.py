"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, session, redirect
from ScoringEngine import app

@app.route('/')
@app.route('/home')
def home():
    if 'user' in session:
        """Renders the home page."""
        return render_template(
            'index.html',
            title='Home Page',
            year=datetime.now().year,
            user=session['user'],
            login='user' in session,
        )
    else:
        return redirect("/login")



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
