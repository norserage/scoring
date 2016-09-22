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
from flask import Flask
app = Flask(__name__)

import ScoringEngine.views.home
import ScoringEngine.views.user
import ScoringEngine.views.admin
import ScoringEngine.views.admin.team
import ScoringEngine.views.admin.user
import ScoringEngine.views.admin.server
import ScoringEngine.views.admin.service
import ScoringEngine.views.admin.event
import ScoringEngine.views.admin.passdb
import ScoringEngine.views.portal
import ScoringEngine.views.inject
import ScoringEngine.views.injectmanager.manage
import ScoringEngine.views.api

def setupApp():
    global app
    from ScoringEngine.conf import conf
    app.debug = conf['debug']
    app.secret_key = conf['secret']
    