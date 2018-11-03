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

@app.route('/report')
def reports():
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

import ScoringEngine.web.views.report.event_total