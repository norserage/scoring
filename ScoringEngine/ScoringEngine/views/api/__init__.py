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