from datetime import datetime
from flask import render_template, request, session, redirect, url_for, escape
from ScoringEngine.web import app
from ScoringEngine.db import Session
import ScoringEngine.db.tables as tables
import ScoringEngine.utils
import ScoringEngine.engine
from pprint import pprint as pp


@app.route('/admin/event')
def events():
    if 'user' in session and session['user']['group'] >= 4:
        dbsession = Session()
        events = dbsession.query(tables.Event).all()
        return render_template(
            'admin/event/list.html',
            title='Events',
            year=datetime.now().year,
            enginestatus=ScoringEngine.engine.running,
            user=session['user'],
            login='user' in session,
            events=events
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

@app.route('/admin/event/add',methods=['GET','POST'])
def addevent():
    if 'user' in session and session['user']['group'] == 5:
        if request.method == 'POST':
            dbsession = Session()
            e = tables.Event()
            e.name = request.form['name']
            dbsession.add(e)
            dbsession.commit()
            return redirect(url_for('events'))
        else:
            return render_template(
                'admin/event/add.html',
                title='Add Event',
                year=datetime.now().year,
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

@app.route('/admin/event/<event>')
def event(event):
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
        events = dbsession.query(tables.Event).filter(tables.Event.id==event)
        if events.count() > 0:
            event = events[0]
            return render_template(
                'admin/event/view.html',
                title=event.name,
                year=datetime.now().year,
                user=session['user'],
                login='user' in session,
                event=event,
            )
        else:
            return render_template(
                'admin/404.html',
                title='404 Team Not Found',
                year=datetime.now().year,
                user=session['user'],
                login='user' in session,
                message="We could not find the team that you were looking for."
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

@app.route('/admin/event/<event>/edit',methods=['GET','POST'])
def editevent(event):
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
        servers = dbsession.query(tables.Server).filter(tables.Server.id == event)
        if servers.count() > 0:
            server = servers[0]
            if request.method == 'POST':
                server.name = request.form['name']
                if request.form['ip3'].strip() == "":
                    server.ip_3 = None
                else:
                    server.ip_3 = request.form['ip3']
                server.ip_4 = request.form['ip4']
                server.enabled = 'enabled' in request.form
                #team.save()
                dbsession.commit()
                return redirect(url_for('server',server=server.id))
            else:
                return render_template(
                    'admin/server/edit.html',
                    title='Edit Team',
                    year=datetime.now().year,
                    user=session['user'],
                    login='user' in session,
                    server=server
                )
        else:
            return render_template(
                'admin/404.html',
                title='404 Server Not Found',
                year=datetime.now().year,
                user=session['user'],
                login='user' in session,
                message="We could not find the server that you were looking for."
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


@app.route('/admin/event/<event>/start')
def startevent(event):
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
        events = dbsession.query(tables.Event).filter(tables.Event.id == event)
        if events.count() > 0:
            event = events[0]
            events = dbsession.query(tables.Event).filter(tables.Event.current == True)
            if events.count() > 0:
                for e in events:
                    e.current = False
                    if e.end == None:
                        e.end = datetime.now()
            event.current = True
            event.start = datetime.now()
            dbsession.commit()
            return redirect(url_for("events"))
        else:
            return render_template(
                'admin/404.html',
                title='404 Server Not Found',
                year=datetime.now().year,
                user=session['user'],
                login='user' in session,
                message="We could not find the server that you were looking for."
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
