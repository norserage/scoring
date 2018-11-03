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
from flask_login import LoginManager
from flaskext.markdown import Markdown
from ScoringEngine.core import config
from ScoringEngine.core.db import getSession, tables
from pydoc import locate
import importlib

app = Flask(__name__)

app.debug = config.get_item("debug")
app.secret_key = config.get_item("secret")

class AnonymousUser:
    @property
    def is_active(self):
        return False

    @property
    def is_authenticated(self):
        return False

    @property
    def is_anonymous(self):
        return True

    @property
    def name(self):
        return "(=^_^=)"

    @property
    def group(self):
        return 0

    @property
    def settings(self):
        return {}


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.anonymous_user = AnonymousUser

Markdown(app)

@login_manager.user_loader
def load_user(user_id):
    user = getSession().query(tables.User).filter(tables.User.id == user_id).first()
    if user:
        return user
    return None

@app.context_processor
def inject_template_vars():
    def menu(str1, str2):
        return "active" if str1 == str2 else ""

    def menu_open(str1, str2):
        return "menu-open" if str1 == str2 else ""

    from ScoringEngine import VERSION, BUILD, BRANCH
    from ScoringEngine.core import config
    from flask import Markup

    return dict(menu=menu, menu_open=menu_open, VERSION=VERSION, BUILD=BUILD, BRANCH=BRANCH, analytics=Markup(config.get_item("analytics/html")))

@app.template_filter('localtime')
def localtime(t):
    if t is None:
        return None
    import datetime
    import pytz
    from flask_login import current_user
    tz = pytz.timezone(config.get_item("default_timezone"))
    if "timezone" in current_user.settings:
        tz = pytz.timezone(current_user.settings['timezone'])
    return t.replace(tzinfo=pytz.UTC).astimezone(tz)


# Setup session provider

def _get_class_from_string(s):
    module_name, class_name = s.rsplit(".", 1)
    module = importlib.import_module(module_name)
    return getattr(module, class_name)


app.session_interface = _get_class_from_string(config.get_item("session_provider"))()


import ScoringEngine.web.views
