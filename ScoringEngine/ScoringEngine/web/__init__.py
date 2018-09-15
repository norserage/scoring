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
from ScoringEngine.core import config
from ScoringEngine.core.db import getSession, tables

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
        return "Anon"

    @property
    def group(self):
        return 0


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    user = getSession().query(tables.User).filter(tables.User.id == user_id).first()
    if user:
        return user
    return None

import ScoringEngine.web.views
