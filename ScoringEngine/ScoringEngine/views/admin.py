from datetime import datetime
from flask import render_template, request, session, redirect
from ScoringEngine import app
from ScoringEngine.db import session
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