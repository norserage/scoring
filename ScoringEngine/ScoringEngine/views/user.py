from datetime import datetime
from flask import render_template
from ScoringEngine import app

@app.route('/login')
def login():
    """Renders the home page."""
    return render_template(
        'user/login.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/user/<name>')
def viewuser(name):
    """Renders the home page."""
    return render_template(
        'user/view.html',
        title='Home Page',
        year=datetime.now().year,
    )

