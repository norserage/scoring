from datetime import datetime
from flask import render_template, request, session, redirect, url_for, escape
from ScoringEngine import app
from ScoringEngine.db import session as dbsession
import ScoringEngine.db.tables as tables
import ScoringEngine.utils
import ScoringEngine.engine
from pprint import pprint as pp

@app.route('/admin')
def admin():
    if 'user' in session and session['user']['group'] == 5:
        return render_template(
            'admin/index.html',
            title='Home Page',
            year=datetime.now().year,
            enginestatus=ScoringEngine.engine.running,
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

@app.route('/admin/team')
def teams():
    if 'user' in session and session['user']['group'] == 5:
        teams = dbsession.query(tables.Team).all()
        """Renders the home page."""
        return render_template(
            'admin/team/list.html',
            title='Home Page',
            year=datetime.now().year,
            enginestatus=ScoringEngine.engine.running,
            user=session['user'],
            login='user' in session,
            teams=teams
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

@app.route('/admin/team/add',methods=['GET','POST'])
def addteam():
    if 'user' in session and session['user']['group'] == 5:
        if request.method == 'POST':
            t = tables.Team()
            t.name = request.form['name']
            t.network = request.form['network']
            t.enabled = 'enabled' in request.form
            dbsession.add(t)
            dbsession.commit()
            return redirect(url_for('teams'))
        else:
            return render_template(
                'admin/team/add.html',
                title='Add Team',
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

@app.route('/admin/team/<team>')
def team(team):
    if 'user' in session and session['user']['group'] == 5:
        teams = dbsession.query(tables.Team).filter(tables.Team.name.ilike(team))
        if teams.count() > 0:
            team = teams[0]
            return render_template(
                'admin/team/view.html',
                title=team.name,
                year=datetime.now().year,
                user=session['user'],
                login='user' in session,
                team=team,
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

@app.route('/admin/team/<team>/addserver',methods=['GET','POST'])
def teamaddserver(team):
    if 'user' in session and session['user']['group'] == 5:
        teams = dbsession.query(tables.Team).filter(tables.Team.name.ilike(team))
        if teams.count() > 0:
            if request.method == 'POST':
                t = tables.Team()
                t.name = request.form['name']
                t.network = request.form['network']
                t.enabled = 'enabled' in request.form
                dbsession.add(t)
                dbsession.commit()
                return redirect(url_for('teams'))
            else:
                return render_template(
                    'admin/team/add.html',
                    title='Add Team',
                    year=datetime.now().year,
                    user=session['user'],
                    login='user' in session,
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

@app.route('/admin/scoring/<flag>')
def adminscoringswitch(flag):
    if 'user' in session and session['user']['group'] == 5:
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

