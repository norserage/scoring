"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)

import ScoringEngine.views.home
import ScoringEngine.views.user
import ScoringEngine.views.admin
import ScoringEngine.views.portal