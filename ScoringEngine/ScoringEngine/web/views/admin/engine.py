from datetime import datetime
from flask import render_template, request, session, redirect, url_for
from ScoringEngine.web import app
from ScoringEngine.core.db import getSession, tables
import ScoringEngine.utils
import ScoringEngine.engine

from ScoringEngine.web.flask_utils import db_user, require_group
from flask_login import current_user, login_required


@app.route('/admin/engine')
@login_required
@require_group(5)
@db_user
def engines():
    dbsession = getSession()
    engines = dbsession.query(tables.Engine).all()
    return render_template(
        'admin/engine/list.html',
        title='Engines',
        year=datetime.now().year,
        engines=engines
    )