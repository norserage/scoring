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
def inject(id):
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
