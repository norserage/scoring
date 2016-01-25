"""
Copyright 2016 Brandon Warner

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from datetime import datetime
from flask import render_template, session, redirect, url_for
from ScoringEngine.web import app

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

@app.route('/favicon.ico')
def favicon():
    """Renders the about page."""
    return app.send_static_file("favicon.ico")
