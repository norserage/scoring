from flask import jsonify, request
from ScoringEngine.web import app
from ScoringEngine.core import config

from ScoringEngine.engine import DBEngineHelper

from json import loads

from functools import wraps

helper = DBEngineHelper()


def require_engine_token(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if 'Authorization' in request.headers:
            if request.headers['Authorization'] == "Bearer %s" % config.get_item("engine/psk"):
                return func(*args, **kwargs)
        return jsonify(error="Not Authorized"), 401
    return decorated_view


@app.route('/api/v0/event/current')
@require_engine_token
def api_v0_event_current():
    return jsonify(helper.get_current_event())


@app.route('/api/v0/password_db/<database>/user/random')
@require_engine_token
def api_v0_password_db_database_user_random(database):
    return jsonify(helper.get_random_user(database))


@app.route('/api/v0/engine/<id>/services')
@require_engine_token
def api_v0_engine_services(id):
    return jsonify(helper.get_engine_services(id))

@app.route('/api/v0/teamserver/<teamserver_id>/service/<service_id>/config_legacy')
@require_engine_token
def api_v0_teamserver_service_legacy_config(teamserver_id, service_id):
    return jsonify(helper.get_service_config_old(teamserver_id, service_id))

@app.route('/api/v0/event/<event>/teamserver/<teamserver>/service/<service>/status', methods=['POST'])
@require_engine_token
def api_v0_save_status(event, teamserver, service):
    if request.is_json:
        import pprint
        pprint.pprint(request.json)
        helper.save_new_service_status(
            event={"id":event},
            service={"team_server_id": teamserver, "service_id": service},
            status=request.json['status'],
            extra_info=request.json['info'],
            engine=request.headers['X-ENGINE-ID']
        )
        return jsonify(status="ok"), 201