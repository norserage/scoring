from datetime import datetime
from flask import render_template, request, session, redirect, url_for, escape
from ScoringEngine import app
from ScoringEngine.db import Session
import ScoringEngine.db.tables as tables
import ScoringEngine.utils
import ScoringEngine.engine
import Crypto.Hash.MD5
from pprint import pprint as pp


@app.route('/admin/user')
def users():
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
        users = dbsession.query(tables.User).all()
        """Renders the home page."""
        return render_template(
            'admin/user/list.html',
            title='Home Page',
            year=datetime.now().year,
            enginestatus=ScoringEngine.engine.running,
            user=session['user'],
            login='user' in session,
            users=users
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

@app.route('/admin/user/add',methods=['GET','POST'])
def adduser():
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
        if request.method == 'POST':
            p = Crypto.Hash.MD5.new()
            p.update(request.form['password'])
            u = tables.User
            u.name = request.form['name']
            u.username = request.form['username']
            u.password = p.hexdigest()
            u.team = request.form['team']
            u.group = request.form['group']
            #pp(request.form)
            dbsession.add(u)
            dbsession.commit()
            return redirect(url_for('users'))
        else:
            teams = dbsession.query(tables.Team).all()
            return render_template(
                'admin/user/add.html',
                title='Add Team',
                year=datetime.now().year,
                user=session['user'],
                login='user' in session,
                teams=teams,
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

@app.route('/admin/user/<user>')
def adminuser(user):
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
        users = dbsession.query(tables.User).filter(tables.User.name.ilike(user))
        if users.count() > 0:
            user = users[0]
            return render_template(
                'admin/user/view.html',
                title=user.name,
                year=datetime.now().year,
                user=session['user'],
                login='user' in session,
                dbuser=user,
            )
        else:
            return render_template(
                'admin/404.html',
                title='404 User Not Found',
                year=datetime.now().year,
                user=session['user'],
                login='user' in session,
                message="We could not find the user that you were looking for."
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

@app.route('/admin/user/<user>/edit',methods=['GET','POST'])
def edituser(user):
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
        teams = dbsession.query(tables.Team).filter(tables.Team.name.ilike(team))
        if teams.count() > 0:
            team = teams[0]
            if request.method == 'POST':
                team.name = request.form['name']
                team.network = request.form['network']
                team.enabled = 'enabled' in request.form
                #team.save()
                dbsession.commit()
                return redirect(url_for('team',team=team.name))
            else:
                return render_template(
                    'admin/user/edit.html',
                    title='Edit Team',
                    year=datetime.now().year,
                    user=session['user'],
                    login='user' in session,
                    team=team
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
