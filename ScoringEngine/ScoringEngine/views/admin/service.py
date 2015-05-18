from datetime import datetime
from flask import render_template, request, session, redirect, url_for, escape
from ScoringEngine.web import app
from ScoringEngine.db import Session
import ScoringEngine.db.tables as tables
import ScoringEngine.utils
import ScoringEngine.engine
from pprint import pprint as pp


@app.route('/admin/service')
def services():
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
        services = dbsession.query(tables.ServiceType).all()
        """Renders the home page."""
        return render_template(
            'admin/service/list.html',
            title='Service Types',
            year=datetime.now().year,
            enginestatus=ScoringEngine.engine.running,
            user=session['user'],
            login='user' in session,
            services=services
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

@app.route('/admin/service/add',methods=['GET','POST'])
def addservice():
    if 'user' in session and session['user']['group'] == 5:
        if request.method == 'POST':
            dbsession = Session()
            st = tables.ServiceType()
            st.name = request.form['name']
            st.tester = request.form['tester']
            dbsession.add(st)
            dbsession.commit()
            return redirect(url_for('services'))
        else:
            return render_template(
                'admin/service/add.html',
                title='Add Service Type',
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


@app.route('/admin/service/<service>/edit',methods=['GET','POST'])
def editservice(service):
    if 'user' in session and session['user']['group'] == 5:
        dbsession = Session()
        services = dbsession.query(tables.ServiceType).filter(tables.ServiceType.id == service)
        if services.count() > 0:
            service = services[0]
            if request.method == 'POST':
                service.name = request.form['name']
                service.tester = request.form['tester']
                dbsession.commit()
                return redirect(url_for('services'))
            else:
                return render_template(
                    'admin/service/edit.html',
                    title='Edit Team',
                    year=datetime.now().year,
                    user=session['user'],
                    login='user' in session,
                    service=service
                )
        else:
            return render_template(
                'admin/404.html',
                title='404 Server Not Found',
                year=datetime.now().year,
                user=session['user'],
                login='user' in session,
                message="We could not find the service that you were looking for."
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
