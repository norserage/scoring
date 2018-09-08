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
from flask import render_template, session
from ScoringEngine.web import app
from ScoringEngine.core.db import Session, engine
import ScoringEngine.core.db.tables as tables
import ScoringEngine.utils
import ScoringEngine.engine


@app.route('/admin')
def admin():
    if 'user' in session and session['user']['group'] >= 4:
        dbsession = Session()
        event = None
        events = dbsession.query(tables.Event).filter(tables.Event.current == True)
        if events.count() > 0:
            event = events[0].id
        return render_template(
            'admin/index.html',
            title='Admin',
            year=datetime.now().year,
            enginestatus=ScoringEngine.engine.running,
            user=session['user'],
            login='user' in session,
            driver=str(engine.driver),
            event=event
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

@app.route('/admin/scoring/<flag>')
def adminscoringswitch(flag):
    if 'user' in session and session['user']['group'] >= 4:
        if flag == "true":
            ScoringEngine.engine.running = True
            ScoringEngine.engine.start()
            return ""
        else:
            ScoringEngine.engine.running = False
            return ""
    else:
        return render_template(
            'errors/403.html',
            title='403 Access Denied',
            year=datetime.now().year,
            user=session['user'],
            login='user' in session,
            message="You do not have permission to use this resource"
        )

