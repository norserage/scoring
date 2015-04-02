from datetime import datetime
from flask import render_template, request, session, redirect
from ScoringEngine import app
from ScoringEngine.db import session as dbsession
import ScoringEngine.db.tables as tables
import ScoringEngine.utils

@app.route('/portal')
def portal():
    """Renders the home page."""
    return render_template(
        'portal/index.html',
        title='Home Page',
        year=datetime.now().year,
        user=session['user'],
        login='user' in session,
    )

