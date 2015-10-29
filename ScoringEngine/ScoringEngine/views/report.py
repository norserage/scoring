from datetime import datetime
from flask import render_template, session, redirect, url_for
from ScoringEngine.web import app





@app.route('/report')
def report():
    if session['user']['group'] >= 3:
        return render_template(
            'report/index.html',
            title='Report',
            year=datetime.now().year,
            message='Norser@g3 Inject Scoring Engine',
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