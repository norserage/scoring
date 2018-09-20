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
from flask import render_template
from ScoringEngine.web import app
from ScoringEngine.core.db import getSession, tables
from ScoringEngine.core.db import tables

from ScoringEngine.web.flask_utils import db_user, require_group
from flask_login import current_user, login_required

@app.route('/inject/<id>')
@login_required
@require_group(1)
@db_user
def inject(id):
    session = getSession()
    #select * from assignedinjects where when < now()
    injects = session.query(tables.AssignedInject).filter(tables.AssignedInject.id == id)
    if injects.count() > 0:
        inject = injects[0]
        return render_template(
            'inject/view.html',
            title=inject.subject,
            year=datetime.now().year,
            inject=inject
        )
