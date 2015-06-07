"""
The flask application package.
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
import ScoringEngine.views.portal
import ScoringEngine.views.inject

def setupApp():
    global app
    from ScoringEngine.conf import conf
    app.debug = conf['debug']
    app.secret_key = conf['secret']