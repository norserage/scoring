from flask_login import current_user
from functools import wraps
from flask import render_template



def require_group(group):
    def inner_require_group(func):
        @wraps(func)
        def decorate_view(*args, **kwargs):
            if current_user.group >= group:
                return func(*args, **kwargs)
            return render_template(
                "errors/403.html",
            )
        return decorate_view
    return inner_require_group


def db_user(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        res = func(*args, **kwargs)
        return res
    return decorated_view