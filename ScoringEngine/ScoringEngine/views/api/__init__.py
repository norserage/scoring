
from datetime import datetime
from flask import render_template, session, redirect, url_for, jsonify, request
from ScoringEngine.web import app
from ScoringEngine.db import tables, Session
from json import dumps

@app.route("/api/test")
def api_test():
    session = Session()
    events = session.query(tables.Event).all()
    return dumps([event.seralize() for event in events])

@app.route("/api/test2")
def api_test2():
    return jsonify(r=request)