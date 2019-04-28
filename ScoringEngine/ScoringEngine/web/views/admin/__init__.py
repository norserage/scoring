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
from ScoringEngine.core.db import getSession, tables, engine
import ScoringEngine.utils

from ScoringEngine.web.flask_utils import db_user, require_group
from flask_login import current_user, login_required

@app.route('/admin')
@login_required
@require_group(4)
@db_user
def admin():
    dbsession = getSession()
    event = None
    events = dbsession.query(tables.Event).filter(tables.Event.current == True)
    if events.count() > 0:
        event = events[0].id
    return render_template(
        'admin/index.html',
        title='Admin',
        year=datetime.now().year,
        driver=str(engine.driver),
        event=event
    )

