from datetime import datetime
from flask import render_template, session, redirect, url_for
from ScoringEngine.web import app
from ScoringEngine.db import Session, tables

@app.route('/inject')
def listinjects():
    session = Session()
    #select * from assignedinjects where when < now()
    injects = session.query(tables.AssignedInject).filter(tables.AssignedInject.when < datetime.now())
    return render_template(
        'inject/list.html',
        title='List Injects',
        year=datetime.now().year,
        user=session['user'],
        login='user' in session,
        injects=injects
    )

@app.route('/inject/{id}')
def listinjects(id):
    session = Session()
    #select * from assignedinjects where when < now()
    injects = session.query(tables.AssignedInject).filter(tables.AssignedInject.id == id)
    if injects.count() > 0:
        inject = injects[0]
        return render_template(
            'inject/view.html',
            title='List Injects',
            year=datetime.now().year,
            user=session['user'],
            login='user' in session,
            inject=inject
        )

import uuid
uuid.UU